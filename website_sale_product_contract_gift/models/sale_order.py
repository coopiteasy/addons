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

    def action_confirm(self):
        """Create contract for gift product"""
        contract_model = self.env["contract.contract"]
        for order in self.filtered("is_gift"):
            line_to_create_contract = order.order_line.filtered(
                lambda r: not r.contract_id and r.product_id.is_gift
            )
            line_to_update_contract = order.order_line.filtered(
                lambda r: (
                    r.contract_id
                    and r.product_id.is_gift
                    and r
                    not in r.contract_id.contract_line_ids.mapped("sale_order_line_id")
                )
            )
            for line in line_to_create_contract:
                contract = contract_model.create(
                    {
                        "partner_id": order.partner_shipping_id,
                        "contract_type": "sale",
                    }
                )
                contract._onchange_contract_type()
                line.create_contract_line(contract)
                line.write({"contract_id": contract.id})
            for line in line_to_update_contract:
                line.create_contract_line(line.contract_id)
        return super().action_confirm()
