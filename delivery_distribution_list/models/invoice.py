from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    deposit_point = fields.Boolean(string="Deposit/Sale", readonly=True)
