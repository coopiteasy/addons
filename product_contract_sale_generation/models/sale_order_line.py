# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    def _compute_qty_to_invoice(self):
        res = super()._compute_qty_to_invoice()
        for line in self:
            if line.order_id.created_from_contract:
                # put back the right quantity to invoice
                line.filtered("product_id.is_contract").update(
                    {"qty_to_invoice": line.product_uom_qty}
                )
        return res
