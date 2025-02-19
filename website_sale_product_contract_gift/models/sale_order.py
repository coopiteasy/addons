# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_gift = fields.Boolean(compute="_compute_is_gift")

    @api.depends("order_line")
    def _compute_is_gift(self):
        """Tell if an order is a gift or not"""
        for order in self:
            order.is_gift = any(order.order_line.mapped("product_id").mapped("is_gift"))

    @api.constrains("order_line")
    def _check_gift_alone(self):
        """Ensure gift are not mixed in a sale order."""
        for order in self:
            at_least_one_gift = any(
                order.order_line.mapped("product_id").mapped("is_gift")
            )
            is_all_gift = all(order.order_line.mapped("product_id").mapped("is_gift"))
            if at_least_one_gift and not is_all_gift:
                raise ValidationError(
                    _(
                        "Cannot add product gift in an order that "
                        "contains other product that are not gifts."
                    )
                )

    def check_product_compatibility(self, product_id):
        warning = super().check_product_compatibility(product_id)
        if not warning:
            product = self.env["product.product"].browse(product_id).exists()
            non_gifts = self.order_line.mapped("product_id").filtered(
                lambda p: not p.is_gift
            )
            is_all_gift = all(self.order_line.mapped("product_id").mapped("is_gift"))
            if product:
                if product.is_gift and non_gifts:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "it's a gift and gift must be purchase seperatly."
                    )
                elif not product.is_gift and is_all_gift:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "it is not a gift and other product are gifts."
                    )
        return warning
