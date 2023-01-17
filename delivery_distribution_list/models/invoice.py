from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    deposit_point = fields.Boolean(string="Deposit/Sale", readonly=True)
