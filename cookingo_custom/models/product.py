# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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
    )
    def _compute_container_volume(self):
        child_portion_attribute_value = self.env.ref("cookingo_custom.child_portion")
        for product in self:
            modifier = 1
            if child_portion_attribute_value in product_template_attribute_value_ids:
                modifier = 0.66
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

    is_meal = fields.Boolean(string="Is Meal?", default=False)

    container_1_volume = fields.Float("Container 1 Volume", digits="Volume")
    container_2_volume = fields.Float("Container 2 Volume", digits="Volume")
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
