# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def get_sepa_dd_payment_mode(self):
        return self.env["account.payment.mode"].search(
            [("payment_method_id.code", "=", "sepa_direct_debit")],
            limit=1,
        )
