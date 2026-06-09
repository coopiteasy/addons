# Copyright 2025 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _get_container_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.product_uom_categ_vol").id)]

    # Container
    is_container = fields.Boolean(string="Is a Container", default=False)
    container_volume = fields.Float(digits="Volume")

    # Meal
    is_meal = fields.Boolean(string="Is a Meal", default=False)
    container_1_volume = fields.Float(digits="Volume")
    container_2_volume = fields.Float(digits="Volume")

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
