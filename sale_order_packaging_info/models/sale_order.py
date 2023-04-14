# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_order_packaging_line_ids = fields.One2many(
        comodel_name="sale.order.packaging.line",
        inverse_name="sale_order_id",
        string="Packaging Lines",
    )
    packaging_amount_total = fields.Monetary(
        string="Packaging Total", compute="_compute_packaging_amount"
    )
    packaging_other_text = fields.Text(string="Other (Packaging)")

    @api.model
    def create(self, vals):
        result = super().create(vals)
        for product in result.company_id.packaging_product_ids:
            self.env["sale.order.packaging.line"].create(
                {
                    "sale_order_id": result.id,
                    "product_id": product.id,
                }
            )
        return result

    @api.depends(
        "sale_order_packaging_line_ids",
        "sale_order_packaging_line_ids.price_subtotal",
    )
    def _compute_packaging_amount(self):
        for order in self:
            order.packaging_amount_total = sum(
                order.sale_order_packaging_line_ids.mapped("price_subtotal")
            )
