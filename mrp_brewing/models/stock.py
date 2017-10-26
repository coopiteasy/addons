# -*- coding: utf-8 -*-
# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models, _, SUPERUSER_ID

class StockMove(models.Model):
    _inherit = "stock.move" 
    
    @api.model
    @api.depends('state')
    def get_on_hand(self):
        for move in self:
            if move.state == 'done':
                move.quantity_after_move = move.product_id.qty_available
    
    quantity_after_move = fields.Integer(string="Quantity",compute="get_on_hand",store=True,readonly=True)
    brew_number = fields.Integer(string="Brew number",readonly=True)


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"
    
    qty_available = fields.Float(related='product_id.qty_available',string='Quantity On Hand',readonly=True)
    

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    qty_available = fields.Float(compute="_compute_qty_available", string='Quantity available',store=True)
    
    @api.multi
    @api.depends('quant_ids')
    def _compute_qty_available(self):
        for lot in self:
            qty_available = 0.0
            for quant in lot.quant_ids.filtered(lambda r: r.location_id.usage == 'internal' and not r.reservation_id):
                qty_available += quant.qty
            lot.qty_available = qty_available

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.multi
    def do_transfer(self):
        super(StockPicking, self).do_transfer()
        for picking in self:
            for move in picking.move_lines:
                move.date = picking.date
