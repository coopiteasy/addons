# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, time, timedelta
from dateutil.rrule import rrule, DAILY
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class ResourceCategory(models.Model):

    _name = 'resource.category'

    name = fields.Char(string="Category name", required=True)
    resources = fields.One2many('resource.resource', 'category_id', string="Resources")


class Resource(models.Model):
    _inherit = 'resource.resource'
    
    category_id = fields.Many2one('resource.category', string="Category")
    state = fields.Selection([('available','Available'),
                              ('unavailable','Unavailable')],
                             string="State", default='available')
    resource_type = fields.Selection([('user','Human'),('material','Material')],
                                      string="Resource Type", required=True, default="material")
    allocations = fields.One2many('resource.allocation', 'resource_id', string="Booking lines")
    serial_number = fields.Char(string="Serial number")

    @api.multi
    def action_unavailable(self):
        for resource in self:
            resource.state = 'unavailable'

    @api.multi
    def action_available(self):
        for resource in self:
            resource.state = 'available'
    
    @api.multi        
    def check_availabilities(self, date_start, date_end):
        if not date_start or not date_end:
            raise ValidationError((_("Error. Date start or date end aren't set")))
        available_resources = self.ids

        date_start = datetime.strptime(date_start, DTF)
        date_end = datetime.strptime(date_end, DTF)
        domain = [('resource_id', 'in', available_resources)]
        domain.append(('state', '!=', 'cancel'))
        domain.append(('date_end', '>=', fields.Datetime.now()))
        domain.append('|')
        domain.append('|')
        domain.append('&')
        domain.append(('date_start', '>=', date_start.strftime(DTF)))
        domain.append(('date_start', '<', date_end.strftime(DTF)))
        domain.append('&')
        domain.append(('date_end', '>', date_start.strftime(DTF)))
        domain.append(('date_end', '<=', date_end.strftime(DTF)))
        domain.append('&')
        domain.append(('date_start', '<=', date_start.strftime(DTF)))
        domain.append(('date_end', '>=', date_end.strftime(DTF)))
        
        #for matching_allocation in self.env['resource.allocation'].search(domain):
        matching_allocations = self.env['resource.allocation'].search(domain)
        resource_ids = matching_allocations.mapped('resource_id.id')
        
            #unavailable_resources = matching_allocations.resource_id.ids
        for resource_id in resource_ids:
            available_resources.remove(resource_id)
        return available_resources
    
    @api.multi
    def allocate_resource(self, allocation_type, date_start, date_end, partner_id, date_lock=False):
        res_alloc = self.env['resource.allocation']
        vals = {
            'date_start':date_start,
            'date_end':date_end,
            'date_lock':date_lock,
            'state':allocation_type,
            'partner_id':partner_id.id
        }
        
        for resource in self:
            vals['resource_id'] = resource.id
            res_alloc.create(vals)

class ResourceAllocation(models.Model):
    _name = 'resource.allocation'
    
    name = fields.Many2one(related="partner_id")
    serial_number = fields.Char(related="resource_id.serial_number", string="Serial number")
    resource_id = fields.Many2one('resource.resource', string="Resource", required=True)
    resource_category_id = fields.Many2one(related='resource_id.category_id', string="Resource Category")
    date_start = fields.Datetime(string="Date start")
    date_end = fields.Datetime(string="Date end")
    state = fields.Selection([('booked','Booked'),
                             ('option','Option'),
                             ('cancel','Cancel')],
                            string="State", default='option')
    date_lock = fields.Date(string="Lock date",
                            help="If the booking type is option, it should be confirmed before the lock date expire")
    partner_id = fields.Many2one('res.partner', string="Partner")

    @api.multi
    def action_confirm(self):
        for allocation in self:
            allocation.state = 'booked'

    @api.multi
    def action_cancel(self):
        for allocation in self:
            allocation.state = 'cancel'

    @api.multi
    def action_option(self):
        for allocation in self:
            allocation.state = 'option'