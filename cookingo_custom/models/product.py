# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _container_domain(self):
        return [
            (
                "categ_id",
                "child_of",
                self.env.ref("cookingo_custom.category_containers").id,
            )
        ]

    is_meal = fields.Boolean(string="Is Meal?", default=False)

    container_1 = fields.Many2one(
        comodel_name="product.template", string="Container 1", domain=_container_domain
    )
    container_2 = fields.Many2one(
        comodel_name="product.template", string="Container 2", domain=_container_domain
    )

