# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    carrier_id = fields.Many2one('res.partner', string="Assigned carrier", readonly=True)
    distribution_list_id = fields.Many2one('delivery.distribution.list', string="Distribution list", readonly=True)
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    carrier_id = fields.Many2one(comodel_name='res.partner', compute='_compute_distribution_fields', string="Assigned carrier", store=True)
    distribution_list_id = fields.Many2one(comodel_name='delivery.distribution.list', compute='_compute_distribution_fields', string="Distribution list", store=True)
    
    @api.multi
    @api.depends('move_lines')
    def _compute_distribution_fields(self):
        for picking in self: 
            if picking.sale_id:
                picking.carrier_id = picking.sale_id.carrier_id
                picking.distribution_list_id = picking.sale_id.distribution_list_id