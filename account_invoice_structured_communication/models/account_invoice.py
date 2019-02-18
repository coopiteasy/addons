# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp

class account_invoice(models.Model):

    _inherit = 'account.invoice'
    
    # global_discount = fields.Float(string='Global discount(%)', digits=dp.get_precision('Discount'), default=0.0)
    
