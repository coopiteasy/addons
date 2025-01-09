# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.http import request

from odoo.addons.website_sale.controllers.main import PaymentPortal


class PaymentPortalSEPADD(PaymentPortal):
    def _validate_transaction_for_order(self, transaction, sale_order_id):
        """Throws a ValidationError if IBAN is not correct"""
        if transaction.provider_id.code == "sepa_dd":
            # Set SEPA Direct Debit payment_mode_id
            order = request.env["sale.order"].sudo().browse(sale_order_id).exists()
            order.payment_mode_id = order.get_sepa_dd_payment_mode()

        return super()._validate_transaction_for_order(transaction, sale_order_id)
