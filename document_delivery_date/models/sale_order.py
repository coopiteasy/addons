# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.multi
    def _prepare_invoice(self):
       invoice_vals = super(SaleOrder, self)._prepare_invoice()
       invoice_vals['commitment_date'] = self.commitment_date
       
       return invoice_vals 