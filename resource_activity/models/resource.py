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
    resource_activity_id = fields.Many2many('resource.activity.type', string="Activity type")


class ResourceLocation(models.Model):
    _inherit = 'resource.location'

    guides = fields.One2many('res.partner', 'resource_location_guide', domain=[('is_guide', '=', True)], string="Guides")
    trainers = fields.One2many('res.partner', 'resource_location_trainer', domain=[('is_trainer', '=', True)], string="Trainers")


class ResourceAllocation(models.Model):
    _inherit = 'resource.allocation'

    activity_registration_id = fields.Many2one('resource.activity.registration', string="Activity registration", readonly=True)
    activity_id = fields.Many2one(related='activity_registration_id.resource_activity_id', string="Activity", readonly=True)
