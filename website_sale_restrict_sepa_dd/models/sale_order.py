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
                        "Cannot add a product that does not allow SEPA "
                        "Direct Debit payments to a sales order containing "
                        "products that allow only SEPA Direct Debit payments."
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

    def check_product_compatibility(self, product_id):
        warning = super().check_product_compatibility(product_id)
        if not warning:
            product = self.env["product.product"].browse(product_id).exists()
            only_sepa_dd_product = self.order_line.mapped("product_id").filtered(
                lambda p: p.only_sepa_dd_payment
            )
            allow_sepa_dd_payment = all(
                self.order_line.mapped("product_id").mapped("allow_sepa_dd_payment")
            )
            if product:
                if only_sepa_dd_product and not product.allow_sepa_dd_payment:
                    # This product cannot be added
                    warning = _(
                        "Product {product_name} cannot be added to the cart "
                        "because product(s): {products} must be paid for by "
                        "SEPA Direct Debit and product {product_name} cannot "
                        "be paid for by such method. Please process this "
                        "order first, or clear it."
                    ).format(
                        product_name=product.name,
                        products=", ".join(p.name for p in only_sepa_dd_product),
                    )
                elif not allow_sepa_dd_payment and product.only_sepa_dd_payment:
                    warning = _(
                        "Product {product_name} cannot be added to the cart "
                        "because other products in the cart do not allow "
                        "SEPA Direct Debit as payment method and "
                        "{product_name} must be paid for by such method. "
                        "Please process this order first, or clear it."
                    ).format(product_name=product.name)
        return warning
