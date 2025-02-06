# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import _, api, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.constrains("order_line")
    def _check_trial_alone(self):
        """Ensure trial are not mixed in a sale order."""
        for order in self:
            at_least_one_trial = any(
                order.order_line.mapped("product_id").mapped("is_trial")
            )
            if at_least_one_trial and order.order_line > 1:
                raise ValidationError(
                    _(
                        "Cannot add product trial in an order that "
                        "contains other products."
                    )
                )

    def check_product_compatibility(self, product_id):
        warning = super().check_product_compatibility(product_id)
        if not warning:
            product = self.env["product.product"].browse(product_id).exists()
            non_trials = self.order_line.mapped("product_id").filtered(
                lambda p: not p.is_trial
            )
            any_trial = any(self.order_line.mapped("product_id").mapped("is_trial"))
            if product:
                if product.is_trial and non_trials:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "it's a trial and trial must be ordered seperately."
                    )
                elif not product.is_trial and any_trial:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "order contains products that are trials and "
                        "trials must be ordered separately."
                    )
        return warning
