# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit='res.partner'
    
    resource_location = fields.Many2one('resource.location', string="Location")

class ResUsers(models.Model):
    _inherit='res.users'

    resource_location = fields.Many2one('resource.location', string="Location")

class ResourceLocation(models.Model):
    _name = 'resource.location'
    
    name = fields.Char(string="Name")
    address = fields.Many2one('res.partner', string="Address")
    customers = fields.One2many('res.partner','resource_location', domain=[('customer','=',True)], string="Customers")
    resources = fields.One2many('resource.resource','location', string="Resources")
    users = fields.One2many('res.users','resource_location', string="Users")
