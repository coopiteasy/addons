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
            lines_to_check = order._exclude_delivery_order_line()
            if not self._is_product_compatible(lines_to_check.product_id):
                raise ValidationError(
                    _(
                        "Cannot add product trial in an order that "
                        "contains other products."
                    )
                )

    @api.model
    def _is_product_compatible(self, product_ids):
        at_least_one_trial = any(product_ids.mapped("is_trial"))
        return not at_least_one_trial or len(product_ids) <= 1

    def _exclude_delivery_order_line(self):
        """Return the order_lines that are not delivery"""
        self.ensure_one()
        return self.order_line.filtered(lambda r: not r.is_delivery)

    def check_product_compatibility(self, product_id):
        warning = super().check_product_compatibility(product_id)
        lines_to_check = self._exclude_delivery_order_line()
        product = self.env["product.product"].browse(product_id).exists()
        if not warning and lines_to_check and product:
            is_product_compatible = self._is_product_compatible(
                lines_to_check.product_id | product
            )
            if not is_product_compatible:
                if product.is_trial:
                    warning = _(
                        f"Product {product.name} cannot be added because "
                        "it's a trial and trials must be ordered separately."
                    )
                else:
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
