# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

CHILD_PORTION_RATIO = 2 / 3


class Product(models.Model):
    _inherit = "product.product"

    # Overrides
    container_1_volume = fields.Float(
        compute="_compute_container_volume",
        digits="Volume",
        store=True,
    )
    container_2_volume = fields.Float(
        compute="_compute_container_volume",
        digits="Volume",
        store=True,
    )

    @api.depends(
        "product_tmpl_id",
        "product_tmpl_id.container_1_volume",
        "product_tmpl_id.container_2_volume",
        "product_template_attribute_value_ids",
    )
    def _compute_container_volume(self):
        try:
            child_portion_attribute_value = self.env.ref(
                "container_meals.product_attribute_portion_size_value_child"
            )
        except ValueError:
            _logger.warning(
                "'container_meals.product_attribute_portion_size_value_child'"
                " does not exist; container volume calculation may misbehave."
            )
            child_portion_attribute_value = self.env["product.attribute.value"]
        for product in self:
            modifier = 1
            if (
                child_portion_attribute_value
                in product.product_template_attribute_value_ids.product_attribute_value_id  # noqa: B950
            ):
                # TODO: Make this configurable.
                modifier = CHILD_PORTION_RATIO
            product.container_1_volume = (
                product.product_tmpl_id.container_1_volume * modifier
            )
            product.container_2_volume = (
                product.product_tmpl_id.container_2_volume * modifier
            )
