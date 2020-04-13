# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from collections import defaultdict

class ResourceCategory(models.Model):
    _inherit = 'resource.category'
    
    product_ids = fields.Many2many('product.product', string="Product")


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _order = 'registration_counter desc'
    
    resource_category_id = fields.Many2many(
        'resource.category',
        string="Resource category")
    resource_activity_id = fields.Many2many(
        'resource.activity.type',
        string="Activity type")
    registration_counter = fields.Integer(
        string='Registration counter',
        default=0,
    )

    @api.model
    def compute_registration_counter(self):
        registrations = (
            self.env['resource.activity.registration']
                .search([('state', '=', 'booked')])
        )
        # could be optimized with sql but
        # early optimisation is the root of all evil

        for registration in registrations.filtered(lambda r: r.sale_order_id):
            product_id = registration.product_id
            if product_id:
                product_id.registration_counter += 1


class ResourceLocation(models.Model):
    _inherit = 'resource.location'

    guides = fields.One2many('res.partner', 'resource_location_guide', domain=[('is_guide', '=', True)], string="Guides")
    trainers = fields.One2many('res.partner', 'resource_location_trainer', domain=[('is_trainer', '=', True)], string="Trainers")
    opening_hours_ids = fields.Many2many('activity.opening.hours', string="Opening Hours")
    terms_conditions_id = fields.Many2one(
        comodel_name="res.company.terms",
        string="Terms and Conditions",
        help="Terms and Conditions related to this location"
    )


class ResourceAllocation(models.Model):
    _inherit = 'resource.allocation'

    activity_registration_id = fields.Many2one('resource.activity.registration', string="Activity registration", readonly=True)
    activity_id = fields.Many2one(related='activity_registration_id.resource_activity_id', string="Activity", readonly=True)
