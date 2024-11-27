# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import _
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.website_sale.controllers.main import PaymentPortal


class PaymentPortalSEPADD(PaymentPortal):
    def _validate_transaction_for_order(self, transaction, sale_order_id):
        """Throws a ValidationError if IBAN is not correct"""
        if (
            transaction.provider_id.code == "custom"
            and transaction.provider_id.custom_mode == "sepa_dd"
        ):
            sepa_dd_accept = request.params.get("sepa_dd_accept")
            if not sepa_dd_accept:
                raise ValidationError(
                    _("You must accept to give a SEPA Direct Debit Mandate.")
                )
            sepa_dd_iban = request.params.get("sepa_dd_iban", "")
            if not sepa_dd_iban:
                raise ValidationError(
                    _("IBAN must be provided for SEPA Direct Debit payment")
                )
            transaction.sepa_dd_iban = sepa_dd_iban

            # Set SEPA Direct Debit payment_mode_id
            order = request.env["sale.order"].sudo().browse(sale_order_id).exists()
            order.payment_mode_id = order.get_sepa_dd_payment_mode()

        return super()._validate_transaction_for_order(transaction, sale_order_id)
