# -*- coding: utf-8 -*-

from openerp import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Related Sale Line',
        compute='_compute_related_order_line',
    )

    currency_id = fields.Many2one(
        related='order_line_id.currency_id')
    price_subtotal = fields.Monetary(
        string='Subtotal',
        related='order_line_id.price_subtotal')
    price_taxes = fields.Monetary(
        string='Taxes',
        related='order_line_id.price_tax')
    price_total = fields.Monetary(
        string='Total',
        related='order_line_id.price_total')

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

    currency_id = fields.Many2one(
        related='order_line_id.currency_id')
    price_subtotal = fields.Monetary(
        string='Subtotal',
        related='order_line_id.price_subtotal')
    price_taxes = fields.Monetary(
        string='Taxes',
        related='order_line_id.price_tax')
    price_total = fields.Monetary(
        string='Total',
        related='order_line_id.price_total')

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
