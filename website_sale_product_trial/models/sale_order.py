# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timedelta

from odoo import _, api, models
from odoo.exceptions import ValidationError

TRIAL_DURATION_DAYS = 14


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

    def _prepare_order_line_values(
        self,
        product_id,
        quantity,
        linked_line_id=False,
        no_variant_attribute_values=None,
        product_custom_attribute_values=None,
        **kwargs,
    ):
        values = super()._prepare_order_line_values(
            product_id=product_id,
            quantity=quantity,
            linked_line_id=linked_line_id,
            no_variant_attirbute_values=no_variant_attribute_values,
        )
        # Hard coded 15 days for trial duration
        product = self.env["product.product"].browse(product_id)
        if product.is_trial:
            values["date_start"] = datetime.today()
            values["date_end"] = datetime.today() + timedelta(days=TRIAL_DURATION_DAYS)
        return values
