# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    carrier_id = fields.Many2one('res.partner', string="Assigned carrier", readonly=True)
    distribution_list_id = fields.Many2one('delivery.distribution.list', string="Distribution list", readonly=True)
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    carrier_id = fields.Many2one('res.partner', string="Assigned carrier", readonly=True)