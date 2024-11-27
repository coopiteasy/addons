# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.addons.base_iban.models.res_partner_bank import validate_iban


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    sepa_dd_iban = fields.Char(string="IBAN (for SEPA Direct Debit)")

    @api.constrains("sepa_dd_iban", "partner_id")
    def _check_sepa_dd_iban(self):
        """Raise ValidationError if sepa_dd_iban is not correct"""
        if self.sepa_dd_iban:
            validate_iban(self.sepa_dd_iban)
            sanitized_sepa_dd_iban = sanitize_account_number(self.sepa_dd_iban)
            res_partner_bank = self.env["res.partner.bank"].search(
                [("sanitized_acc_number", "=", sanitized_sepa_dd_iban)],
                limit=1,
            )
            if res_partner_bank and res_partner_bank.partner_id != self.partner_id:
                raise ValidationError(
                    f"The account number {sanitized_sepa_dd_iban} does not belongs "
                    f"to {self.partner_id.name}."
                )
            return res_partner_bank

    def _set_pending(self, state_message=None):
        txs_to_process = super()._set_pending(state_message=state_message)
        txs_to_process.create_sepa_dd_mandate()
        return txs_to_process

    def get_res_partner_bank(self):
        """Return res.partner.bank that match the sepa_dd_iban
        account.
        """
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
                res_partner_bank = self.env["res.partner.bank"].create(
                    {
                        "partner_id": tx.partner_id.id,
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
