# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    @api.model
    def get_container_deposit_product_id(self):
        deposit_product_id = self.sudo().get_param(
            "container_meals.container_deposit_product_id"
        )
        return self.env["product.product"].browse(int(deposit_product_id))
