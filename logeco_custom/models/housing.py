from odoo import fields, models


class Housing(models.Model):
    _inherit = "hc.housing"

    floor_oclp = fields.Integer(string="OCLP Floor number", required=False)
