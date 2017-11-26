# -*- coding: utf-8 -*-

from openerp import _, api, fields, models

class ResCompany(models.Model):
    
    _inherit = 'res.company'
    
    operational_site = fields.Many2one('res.partner', string="Operational site")
