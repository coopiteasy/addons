# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_sepa_dd_payment = fields.Boolean(compute="_compute_is_sepa_dd_payment")

    def _compute_is_sepa_dd_payment(self):
        payment_mode = self.env["account.payment.mode"].search(
            [("payment_method_id.code", "=", "sepa_direct_debit")],
            limit=1,
        )
        for order in self:
            order.is_sepa_dd_payment = payment_mode == order.payment_mode_id
