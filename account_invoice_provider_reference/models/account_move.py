from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    provider_reference = fields.Char(string="Provider Reference Invoice")
