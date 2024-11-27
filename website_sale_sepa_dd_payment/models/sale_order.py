# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    allow_sepa_dd_payment = fields.Boolean(compute="_compute_allow_sepa_dd_payment")

    @api.depends("order_line", "payment_mode_id")
    def _compute_allow_sepa_dd_payment(self):
        for order in self:
            only_allowed = all(
                order.order_line.mapped("product_id").mapped("allow_sepa_dd_payment")
            )
            order.allow_sepa_dd_payment = only_allowed

    def get_sepa_dd_payment_mode(self):
        return self.env["account.payment.mode"].search(
            [("payment_method_id.code", "=", "sepa_direct_debit")],
            limit=1,
        )
