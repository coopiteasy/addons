# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp

class account_invoice(models.Model):

    _inherit = 'account.invoice'
    
    global_discount = fields.Float(string='Global discount(%)', digits=dp.get_precision('Discount'), default=0.0)
    
    @api.one
    def propagate_discount_on_lines(self):
        for line in self.invoice_line_ids:
            line.discount = self.global_discount
        
        self.compute_taxes()