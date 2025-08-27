# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.addons.base_iban.models.res_partner_bank import validate_iban
from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)


# Similar to payment_custom and payment_authorize"""
class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    sepa_dd_iban = fields.Char(string="IBAN (for SEPA Direct Debit)")

    # Override

    def _get_specific_processing_values(self, processing_values):
        """Override of payment to return an access token as
        provider-specific processing values.
        """
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != "sepa_dd":
            return res

        return {
            "access_token": payment_utils.generate_access_token(
                processing_values["reference"], processing_values["partner_id"]
            )
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Override of payment to find the transaction based on custom data.

        :param str provider_code: The code of the provider that handled
                                  the transaction
        :param dict notification_data: The notification feedback data
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != "sepa_dd" or len(tx) == 1:
            return tx

        reference = notification_data.get("reference")
        tx = self.search(
            [("reference", "=", reference), ("provider_code", "=", "sepa_dd")]
        )
        if not tx:
            raise ValidationError(
                _(
                    "SEPA Direct Debit: No transaction found matching reference %s.",
                    reference,
                )
            )
        return tx

    def _process_notification_data(self, notification_data):
        """Override of payment to process the transaction based on custom data.

        Note: self.ensure_one()

        :param dict notification_data: The custom data
        :return: None
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != "sepa_dd":
            return

        if not notification_data.get("sepa_dd_accept"):
            raise ValidationError(
                _("You must accept terms to give a SEPA Direct Debit Mandate.")
            )
        if not notification_data.get("sepa_dd_iban"):
            raise ValidationError(
                _("IBAN must be provided for SEPA Direct Debit payment")
            )
        self.sepa_dd_iban = notification_data.get("sepa_dd_iban", "")
        self._set_pending()
        _logger.info(
            "validated sepa_dd payment for transaction with reference %s: set as pending",
            self.reference,
        )

    def _log_received_message(self):
        """Override of `payment` to remove custom providers from the recordset.

        :return: None
        """
        other_provider_txs = self.filtered(lambda t: t.provider_code != "sepa_dd")
        return super(PaymentTransaction, other_provider_txs)._log_received_message()

    def _get_sent_message(self):
        """Override of payment to return a different message.

        :return: The 'transaction sent' message
        :rtype: str
        """
        message = super()._get_sent_message()
        if self.provider_code == "custom":
            message = _(
                "The customer has selected %(provider_name)s to make the payment.",
                provider_name=self.provider_id.name,
            )
        return message

    def _set_pending(self, state_message=None):
        """Create mandate when transaction is set as pending"""
        txs_to_process = super()._set_pending(state_message=state_message)
        if self.provider_code == "sepa_dd":
            txs_to_process.create_sepa_dd_mandate()
        return txs_to_process

    # Constrains

    @api.constrains("sepa_dd_iban", "partner_id")
    def _check_sepa_dd_iban(self):
        """Raise ValidationError if sepa_dd_iban is not correct"""
        if self.sepa_dd_iban:
            validate_iban(self.sepa_dd_iban)
            res_partner_bank = self.get_res_partner_bank()
            if (
                res_partner_bank
                and res_partner_bank.partner_id.commercial_partner_id
                != self.partner_id.commercial_partner_id
            ):
                raise ValidationError(
                    f"The account number {res_partner_bank.acc_number} does not belongs "
                    f"to {self.partner_id.name}."
                )
            return res_partner_bank

    # Custom methods

    def get_res_partner_bank(self):
        """Return res.partner.bank that match the sepa_dd_iban account."""
        self.ensure_one()
        res_partner_bank = self.env["res.partner.bank"]
        if self.sepa_dd_iban:
            sanitized_sepa_dd_iban = sanitize_account_number(self.sepa_dd_iban)
            res_partner_bank = self.env["res.partner.bank"].search(
                [("sanitized_acc_number", "=", sanitized_sepa_dd_iban)],
                limit=1,
            )
        return res_partner_bank

    def sepa_dd_mandate_vals(self):
        self.ensure_one()
        return {
            "format": "sepa",
            "type": "recurrent",
            "scheme": "CORE",
            "recurrent_sequence_type": "recurring",
            "signature_date": datetime.datetime.now(),
            "state": "valid",
        }

    def create_sepa_dd_mandate(self):
        for tx in self:
            res_partner_bank = tx.get_res_partner_bank()
            if not res_partner_bank:
                # force parent company creation to attach the bank account to it
                partner = tx.partner_id
                if (
                    not partner.parent_id
                    and not partner.is_company
                    and partner.company_name
                ):
                    partner.create_company()
                res_partner_bank = self.env["res.partner.bank"].create(
                    {
                        "partner_id": partner.commercial_partner_id.id,
                        "acc_number": tx.sepa_dd_iban,
                    }
                )
            res_partner_bank.write(
                {
                    "mandate_ids": [
                        (0, 0, tx.sepa_dd_mandate_vals()),
                    ],
                }
            )
