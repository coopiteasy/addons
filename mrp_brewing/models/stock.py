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

    quantity_after_move = fields.Integer(
        string="Quantity",
        compute="get_on_hand",
        store=True,
        readonly=True)
    brew_number = fields.Integer(
        string="Brew number",
        readonly=True)


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(
        related='product_id.qty_available',
        string='Quantity On Hand',
        readonly=True)


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    _order = 'has_stock desc, create_date asc'

    qty_available = fields.Float(
        string='Quantity available',
        compute="_compute_qty_available",
        store=True)

    has_stock = fields.Boolean(
        string='Has Stock',
        compute="_compute_qty_available",
        store=True,
    )

    @api.multi
    @api.depends('quant_ids.reservation_id')
    def _compute_qty_available(self):
        for lot in self:
            quants = lot.quant_ids.filtered(
                lambda r: r.location_id.usage == 'internal' and not r.reservation_id)  # noqa
            qty = sum(quants.mapped('qty'))
            lot.qty_available = qty
            lot.has_stock = qty > 0

    @api.model
    def _batch_compute_qty_available(self):
        lots = self.env['stock.production.lot'].search([])
        lots._compute_qty_available()


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_transfer(self):
        super(StockPicking, self).do_transfer()
        for picking in self:
            for move in picking.move_lines:
                move.date = picking.date
