# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError

class ResourceCategory(models.Model):
    _inherit = 'resource.category'
    
    product_ids = fields.Many2many('product.product', string="Product")
    
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    resource_category_id = fields.Many2many('resource.category', string="Resource category")