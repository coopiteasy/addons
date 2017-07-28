# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    deposit_point = fields.Boolean(string="Deposit/Sale", readonly=True)
    