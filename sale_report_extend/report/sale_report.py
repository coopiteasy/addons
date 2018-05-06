# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class SaleReport(models.Model):
    _inherit = "sale.report"
    
    category_id = fields.Many2one('res.partner.category', string='Partner Category', readonly=True)

    def _select(self):
        return  super(SaleReport, self)._select() + ", pcr.category_id as category_id"
    
    def _from(self):
        return  super(SaleReport, self)._from() + " left join res_partner_res_partner_category_rel pcr on (pcr.partner_id=s.partner_id)"
            
    def _group_by(self):
        return  super(SaleReport, self)._group_by() + ", pcr.category_id"
            
