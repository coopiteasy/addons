# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class SaleOrderPackagingLine(models.Model):
    _name = "sale.order.packaging.line"
    _description = "Sale Order Packaging Lines"

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
        related="product_id.uom_id",
    )
    product_uom_qty = fields.Float(
        string="Quantity",
        digits="Product Unit of Measure",
        default=0,
        required=True,
    )
    currency_id = fields.Many2one(
        related="sale_order_id.currency_id", string="Currency"
    )
    price_unit = fields.Float(
        string="Unit Price",
        related="product_id.lst_price",
        digits="Product Price",
    )
    price_subtotal = fields.Monetary(
        string="Subtotal", compute="_compute_price_subtotal"
    )
    sequence = fields.Integer(default=10)

    @api.depends("price_unit", "product_uom_qty")
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.product_uom_qty

    # this is a copy of sale.order.line._convert_to_tax_base_line_dict(), with
    # taxes and discount removed.
    def _convert_to_tax_base_line_dict(self):
        """
        Convert the current record to a dictionary in order to use the generic
        taxes computation method defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env["account.tax"]._convert_to_tax_base_line_dict(
            self,
            partner=self.sale_order_id.partner_id,
            currency=self.sale_order_id.currency_id,
            product=self.product_id,
            price_unit=self.price_unit,
            quantity=self.product_uom_qty,
            price_subtotal=self.price_subtotal,
        )
