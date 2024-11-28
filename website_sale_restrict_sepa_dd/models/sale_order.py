# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    allow_sepa_dd_payment = fields.Boolean(compute="_compute_allow_sepa_dd_payment")
    only_sepa_dd_payment = fields.Boolean(compute="_compute_only_sepa_dd_payment")

    @api.constrains("order_line")
    def _check_compatible_product(self):
        """Prevent incompatible product to be added to the same sale order"""
        for order in self:
            only_sepa_dd_payment = any(
                order.order_line.mapped("product_id").mapped("only_sepa_dd_payment")
            )
            allow_sepa_dd_payment = all(
                order.order_line.mapped("product_id").mapped("allow_sepa_dd_payment")
            )
            if only_sepa_dd_payment and not allow_sepa_dd_payment:
                raise ValidationError(
                    _(
                        "Cannot add product that does not allow SEPA "
                        "Direct Debit with products that allow only SEPA "
                        "Direct Debit payment."
                    )
                )

    @api.depends("order_line")
    def _compute_allow_sepa_dd_payment(self):
        for order in self:
            allow_sepa_dd_payment = all(
                order.order_line.mapped("product_id").mapped("allow_sepa_dd_payment")
            )
            order.allow_sepa_dd_payment = allow_sepa_dd_payment

    @api.depends("order_line")
    def _compute_only_sepa_dd_payment(self):
        for order in self:
            order.only_sepa_dd_payment = any(
                order.order_line.mapped("product_id").mapped("only_sepa_dd_payment")
            )

    def _cart_update(self, product_id, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Prevent incompatible product to be added to the cart."""
        self.ensure_one()
        product = self.env["product.product"].browse(product_id).exists()
        warning = ""
        if product:
            only_sepa_dd_product = self.order_line.mapped("product_id").filtered(
                lambda p: p.only_sepa_dd_payment
            )
            allow_sepa_dd_payment = all(
                self.order_line.mapped("product_id").mapped("allow_sepa_dd_payment")
            )
            if only_sepa_dd_product and not product.allow_sepa_dd_payment:
                # This product cannot be added
                add_qty, set_qty = None, 0
                warning = _(
                    f"Product {product.name} cannot be added to cart "
                    "because product(s) : "
                    f"{', '.join(p.name for p in only_sepa_dd_product)} "
                    "must be payed by SEPA Direct Debit and product "
                    f"{product.name} cannot be payed by such method."
                )
            elif not allow_sepa_dd_payment and product.only_sepa_dd_payment:
                add_qty, set_qty = None, 0
                warning = _(
                    f"Product {product.name} cannot be added to cart "
                    "because other products in the cart does not allow "
                    "SEPA Direct Debit as payment method and "
                    f"{product.name} must be payed with such a method."
                )

        values = super()._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            **kwargs,
        )
        values["warning"] = warning
        return values
