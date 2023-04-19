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
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        company_id = result.get("company_id")
        if company_id:
            # price_unit is specified here because it will show as empty if I
            # don't. I don't know why, but it's no problem.
            result["sale_order_packaging_line_ids"] = [
                (0, False, {"product_id": product.id, "price_unit": product.lst_price})
                for product in self.env["res.company"]
                .browse(company_id)
                .packaging_product_ids
            ]
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
