# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "product.product"

    # Overrides
    container_1_volume = fields.Float(
        "Container 1 Volume",
        compute="_compute_container_volume",
        digits="Volume",
        store=True,
    )
    container_2_volume = fields.Float(
        "Container 2 Volume",
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
                "cookingo_custom.product_attribute_portion_size_value_child"
            )
        except ValueError:
            _logger.warning(
                "'cookingo_custom.product_attribute_portion_size_value_child'"
                " does not exist; container volume calculation may misbehave."
            )
            child_portion_attribute_value = self.env["product.attribute.value"]
        for product in self:
            modifier = 1
            if (
                child_portion_attribute_value
                in product.product_template_attribute_value_ids.product_attribute_value_id
            ):
                # TODO: Make this configurable.
                modifier = 2 / 3
            product.container_1_volume = (
                product.product_tmpl_id.container_1_volume * modifier
            )
            product.container_2_volume = (
                product.product_tmpl_id.container_2_volume * modifier
            )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _get_container_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.product_uom_categ_vol").id)]

    # Container
    is_container = fields.Boolean(string="Is Container?", default=False)
    container_volume = fields.Float("Container Volume", digits="Volume")

    # Meal
    is_meal = fields.Boolean(string="Is Meal?", default=False)
    container_1_volume = fields.Float("Container 1 Volume", digits="Volume")
    container_2_volume = fields.Float("Container 2 Volume", digits="Volume")

    # Common
    container_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Container Unit of Measure",
        domain=lambda self: self._get_container_uom_domain(),
        default=lambda self: self.env.ref("uom_extra_data.product_uom_millilitre"),
    )
    container_uom_name = fields.Char(
        string="Container Unit of Measure Name",
        related="container_uom_id.name",
        readonly=True,
    )
