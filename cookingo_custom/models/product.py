# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_meal = fields.Boolean(string="Is Meal?", default=False)
