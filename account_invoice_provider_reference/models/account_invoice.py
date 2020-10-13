from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    provider_reference = fields.Char(string="Provider Reference Invoice")
