# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    producer = fields.Char(string="Producer", translate=True)
    total_excluding_vat_by_unit = fields.Monetary(
        string="Total Sales Price excluding VAT by Reference Unit",
        currency_field="currency_id",
    )
