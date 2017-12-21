# -*- coding: utf-8 -*-
from openerp import models, fields, api

class ProductRelease(models.Model):
    _name = "product.release.list"

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids
    
#     @api.multi
#     def _compute_picking_ids(self):
#         for product_release in self:
#             #product_release.picking_ids = self.env['stock.picking'].search([('group_id', '=', order.procurement_group_id.id)]) if order.procurement_group_id else []
#             product_release.delivery_count = len(order.picking_ids)
                
    name = fields.Char(string="Name", copy=False)
    release_date = fields.Date(string='Product Release Date', readonly=True, required=True, index=True, states={'draft': [('readonly', False)]})
    create_date = fields.Date(string='Creation Date', readonly=True, help="Date on which product release list is created.", copy=False, default=fields.Datetime.now)
    
    user_id = fields.Many2one('res.users', string='Release responsible', copy=False, default=lambda self: self.env.user)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok','=',True)], required=True, readonly=True, states={'draft': [('readonly', False)]})
    product_release_lines = fields.One2many('product.release.line','product_release_list', string="Product release lines", copy=False)
#    journal_id = fields.Many2one('account.journal', string="Journal", domain=[('type','=','sale')], required=True)
    release_qty = fields.Integer(string="Product release quantity", required=True, default=1)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ], string='State', readonly=True, copy=False, default='draft')
    
    picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        string='Shipping Policy', required=True, readonly=True, default='direct',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    #picking_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids', string='Picking associated to this release')
    #delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    
    @api.one
    def action_draft(self):
        self.product_release_lines.unlink()
        self.state = 'draft'
    
    @api.one
    def action_cancel(self):
        self.product_release_lines.unlink()
        if self.state in ['draft','validated']:
            self.state = 'cancelled'
    
    @api.one    
    def action_validate(self):
        prod_sub_obj = self.env['product.subscription.object']
        release_line_obj = self.env['product.release.line']
        
        vals = {'state':'validated'}
        if self.name == '' or not self.name:
            prod_rel_seq = self.env.ref('product_subscription.sequence_product_release', False)
            vals['name'] = prod_rel_seq.next_by_id()         
        
        subscriptions = prod_sub_obj.search([('counter','>',0)])
        
        line_vals = {'product_release_list':self.id,
                'product_id':self.product_id.id}
        
        for subscription in subscriptions:
            line_vals['subscriber'] = subscription.subscriber.id
            line_vals['product_subscription'] = subscription.id
            release_line_obj.create(line_vals)
        self.write(vals)
    
    @api.one
    def action_done(self):
        picking_type = self.env['stock.picking.type'].search([('code','=','outgoing')])
        
        vals = {'picking_type_code':'outgoing',
                'origin':self.name,
                'move_type':self.picking_policy,
                'picking_type_id':picking_type.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id':picking_type.default_location_dest_id.id}

        stock_move_vals = {
            'name':'/',
            'product_id':self.product_id.id,
            'product_uom':self.product_id.uom_id.id,
            'product_uom_qty':self.release_qty,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id':picking_type.default_location_dest_id.id}
        
        for line in self.product_release_lines:
            if line.product_subscription.counter > 0:
                picking = line.create_picking(vals,stock_move_vals)
                line.product_subscription.counter = line.product_subscription.counter - 1
        
        for picking in self.product_release_lines.picking:
            if picking.state not in ['cancel','done']:
                if picking.state != 'assigned':
                    picking.recheck_availability()
                    if picking.state != 'assigned':
                        raise UserError(_('Not enough stock to deliver! Please check that there is sufficient product available'))
                for pack_operation in picking.pack_operation_ids:
                    if pack_operation.product_id.id == self.product_id.id:
                        pack_operation.qty_done = self.release_qty
                picking.do_transfer()
        self.state = 'done'
    
        
class ProductReleaseLine(models.Model):
    _name = "product.release.line"
    
    product_release_list = fields.Many2one('product.release.list', string="Product release list", required=True)
    subscriber = fields.Many2one('res.partner', string="Subscriber", domain=[('subscriber','=',True)], required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_subscription = fields.Many2one('product.subscription.object', string='Subscription', required=True)
    counter = fields.Float(related='product_subscription.counter', string="Counteur", readonly=True)
    picking = fields.Many2one('stock.picking', string="Delivery order")
    
    @api.model    
    def create_picking(self, vals, stock_move_vals):
        picking_obj = self.env['stock.picking']
        pack_op_obj = self.env['stock.pack.operation']
        stock_move_obj = self.env['stock.move']
         
        vals['partner_id'] = self.subscriber.id
        
        picking = picking_obj.create(vals)
        stock_move_vals['picking_id'] = picking.id
        stock_move_obj.create(stock_move_vals)
        
        self.picking = picking
        