# -*- coding: utf-8 -*-

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        compute='_compute_related_sale_order',
        # store=True,
    )
    volume = fields.Float(
        string='Order Volume (m³)',
        compute='_compute_related_sale_order',
        # store=True,
    )

    @api.model
    @api.depends('origin')
    def _compute_related_sale_order(self):
        for picking in self:
            sale_order = (
                self.env['sale.order']
                    .search([('name', '=', picking.origin)])
            )
            sale_order.compute_order_volume()
            sale_order.compute_product_category_volumes()

            picking.sale_order_id = sale_order
            picking.volume = sale_order.volume


class StockMove(models.Model):
    _inherit = 'stock.move'

    order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Related Sale Line',
        compute='_compute_related_order_line',
    )

    @api.multi
    @api.depends('picking_id.origin')
    def _compute_related_order_line(self):
        for move in self:
            origin = move.picking_id.origin
            sale_order = (
                self.env['sale.order']
                    .search([('name', '=', origin)])
            )
            order_line = (
                sale_order.order_line
                          .filtered(
                            lambda line: line.product_id == move.product_id)
            )
            move.order_line_id = order_line


class StockPackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Related Move Line',
        compute='_compute_related_order_line',
    )

    @api.multi
    @api.depends('picking_id.origin')
    def _compute_related_order_line(self):
        for operation in self:
            origin = operation.picking_id.origin
            sale_order = (
                self.env['sale.order']
                    .search([('name', '=', origin)])
            )
            order_line = (
                sale_order.order_line
                          .filtered(
                            lambda line: line.product_id == operation.product_id)
            )
            operation.order_line_id = order_line
