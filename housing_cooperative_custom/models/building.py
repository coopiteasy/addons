from odoo import fields, models


class Building(models.Model):
    _inherit = 'hc.building'

    country_id = fields.Many2one(
        default=43)
