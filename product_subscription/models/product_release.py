# -*- coding: utf-8 -*-
from openerp import models, fields, api

class ProductRelease(models.Model):
    _name = "product.release.list"
    
    name = fields.Char(string="Name", copy=False)
    release_date = fields.Date(string='Product Release Date', readonly=True, required=True, index=True, states={'draft': [('readonly', False)]})
    create_date = fields.Date(string='Creation Date', readonly=True, help="Date on which product release list is created.", copy=False, default=fields.Datetime.now)
    
    user_id = fields.Many2one('res.users', string='Release responsible', copy=False, default=lambda self: self.env.user)
    product_id = fields.Many2one('product.template', string='Product', domain=[('sale_ok','=',True)], required=True, readonly=True, states={'draft': [('readonly', False)]})
    product_release_lines = fields.One2many('product.release.line','product_release_list', string="Product release lines", copy=False)
    journal_id = fields.Many2one('account.journal', string="Journal", domain=[('type','=','sale')], required=True)
    release_qty = fields.Integer(string="Product release quantity", required=True, default=1)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ], string='State', readonly=True, copy=False, default='draft')
    
class ProductReleaseLine(models.Model):
    _name = "product.release.line"
    
    product_release_list = fields.Many2one('product.release.list', string="Product release list", required=True)
    partner_id = fields.Many2one('res.partner', string="Subscriber", domain=[('subscriber','=',True)], required=True)
    product_id = fields.Many2one('product.template', string='Product', required=True)
    product_uom = fields.Many2one(related='product_id.uom_id', string='Unit of Measure', readonly=True)
