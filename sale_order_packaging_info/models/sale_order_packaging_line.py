# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class SaleOrderPackagingLine(models.Model):
    _name = "sale.order.packaging.line"

    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sales Order",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Packaging Product",
        required=True,
    )
    product_uom = fields.Many2one(
        "uom.uom",
        string="Unit of Measure",
        default=lambda self: self.product_id.uom_id,
        required=True,
    )
    product_uom_qty = fields.Float(
        string="Quantity",
        digits=dp.get_precision("Product Unit of Measure"),
        default=0,
        required=True,
    )
    currency_id = fields.Many2one(
        related="sale_order_id.currency_id", string="Currency"
    )
    price_unit = fields.Float(
        string="Unit Price",
        related="product_id.lst_price",
        digits=dp.get_precision("Product Price"),
    )
    price_subtotal = fields.Monetary(
        string="Subtotal", compute="_compute_price_subtotal"
    )
    sequence = fields.Integer(string="Sequence", default=10)

    @api.onchange("product_id")
    def _onchange_product_id(self):
        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals["product_uom"] = self.product_id.uom_id
            vals["product_uom_qty"] = self.product_uom_qty or 0
        self.update(vals)

    @api.depends("price_unit", "product_uom_qty")
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.product_uom_qty
