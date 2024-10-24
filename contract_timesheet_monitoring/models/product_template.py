# Copyright 2023 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_support_product = fields.Boolean()
    hours_available = fields.Integer(
        string="Hours available",
        default=0,
    )
