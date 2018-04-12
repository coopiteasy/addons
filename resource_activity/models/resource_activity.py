# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from datetime import date
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    resource_location_guide = fields.Many2one('resource.location', string="Guide Location")
    resource_location_trainer = fields.Many2one('resource.location', string="Trainer location")

class ResourceLocation(models.Model):
    _inherit = 'resource.location'

    guides = fields.One2many('res.partner','resource_location_guide', domain=[('is_guide','=',True)], string="Guides")
    trainers = fields.One2many('res.partner','resource_location_trainer', domain=[('is_trainer','=',True)], string="Trainers")

class ResourceAllocation(models.Model):
    _inherit = 'resource.allocation'

    activity_registration_id = fields.Many2one('resource.activity.registration', string="Activity registration")

class ResourceActivityType(models.Model):
    _name = 'resource.activity.type'
    
    name = fields.Char(string="Type", required=True)
    code = fields.Char(string="Code")

class ResourceActivityTheme(models.Model):
    _name = 'resource.activity.theme'
    
    name = fields.Char(string="Type", required=True)
    code = fields.Char(string="Code")

class ResourceActivityLang(models.Model):
    _name = 'resource.activity.lang'
    
    name = fields.Char(string="Lang", required=True)
    code = fields.Char(string="Code")
    
class ResourceActivity(models.Model):
    _name = 'resource.activity'

    _inherit = ['mail.thread']
    
    name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner', string="Customer", domain=[('customer','=',True)])
    date_start = fields.Datetime(string="Date start", required=True)
    date_end = fields.Datetime(string="Date end", required=True)
    registrations = fields.One2many('resource.activity.registration', 'resource_activity_id', string="Registration")
    location_id = fields.Many2one('resource.location', string="Location", required=True)
    state = fields.Selection([('draft','Draft'),
                              ('option','Option'),
                              ('confirmed','Confirmed'),
                              ('done','Done'),
                              ('cancelled','Cancelled')], string="State", default='draft')
    date_lock = fields.Date(string="Date lock")
    booking_type = fields.Selection([('option','Option'),
                                    ('booked','Booking')], string="Booking type", default='booked')
    active = fields.Boolean('Active')
    departure = fields.Char(string="Departure")
    arrival = fields.Char(string="Arrival")
    description = fields.Char(string="Description")
    comment = fields.Char(string="Comment")
    activity_type = fields.Many2one('resource.activity.type', string="Activity type")
    guides = fields.Many2many('res.partner', string="Guide", domain=[('is_guide','=',True)])
    trainers = fields.Many2many('res.partner', string="Trainer", domain=[('is_trainer','=',True)])
    langs = fields.Many2many('resource.activity.lang', string="Langs")
    activity_theme = fields.Many2one('resource.activity.theme', string="Activity theme")
    need_delivery = fields.Boolean(string="Need delivery?")
    delivery_place = fields.Char(string="Delivery place")
    delivery_time = fields.Char(string="Delivery time")
    registrations_max = fields.Integer(string="Maximum registration")
    registrations_min = fields.Integer(string="Minimum registration")
    registrations_booked = fields.Integer(string="Registration booked",
                        store=True, readonly=True, compute='_compute_registrations')
    registrations_option = fields.Integer(string="Registration option",
                        store=True, readonly=True, compute='_compute_registrations')
    registrations_available = fields.Integer(string="Available registrations",
                        store=True, readonly=True, compute='_compute_registrations')
    registrations_expected = fields.Integer(string="Expected registrations",
                        store=True, readonly=True, compute='_compute_registrations')
    registrations_unconfirmed = fields.Integer(string="Unconfirmed registrations",
                        store=True, readonly=True, compute='_compute_registrations')
    
    @api.onchange('location_id')
    def onchange_location_id(self):
        if self.location_id and self.location_id.address:
            self.departure = self.location_id.address._display_address(self.location_id.address)
            self.arrival = self.location_id.address._display_address(self.location_id.address)

    @api.one
    @api.constrains('date_start','date_end')
    def _check_date(self):
        if self.date_start < fields.Date().today() or self.date_end < fields.Date().today():
            raise ValidationError("Date can't be in the past: %s %s" % (self.date_start,self.date_end))
        if  self.date_end < self.date_start:
            raise ValidationError("Date end can't be before date start: %s %s" % (self.date_start,self.date_end))

    @api.multi
    @api.depends('registrations_max', 'registrations.state')
    def _compute_registrations(self):
        # aggregate registrations by activity and by state
        if self.ids:
            state_field = {
                'draft': 'registrations_unconfirmed',
                'option': 'registrations_option',
                'booked': 'registrations_booked',
            }
            query = """ SELECT resource_activity_id, state, count(resource_activity_id)
                        FROM resource_activity_registration
                        WHERE resource_activity_id IN %s AND state IN ('draft', 'option', 'booked')
                        GROUP BY resource_activity_id, state
                    """
            self._cr.execute(query, (tuple(self.ids),))
            for activity_id, state, num in self._cr.fetchall():
                activity = self.browse(activity_id)
                activity[state_field[state]] += num
        # compute available_registrations
        for activity in self:
            if activity.registrations_max > 0:
                activity.registrations_available = activity.registrations_max - (activity.registrations_option + activity.registrations_booked)
            activity.registrations_expected = activity.registrations_unconfirmed + activity.registrations_option + activity.registrations_booked

    @api.multi
    def action_confirm(self):
        vals = {'state': 'confirmed'}
        res_acti_seq = self.env.ref('resource_activity.sequence_resource_activity', False)
        
        for activity in self:
            if activity.name == '' or not activity.name:
                vals['name'] = res_acti_seq.next_by_id()
            
            activity.write(vals)

    @api.multi
    def action_search(self):
        for activity in self:
            activity.mapped()
    
    @api.multi
    def action_done(self):
        self.state = 'done'          
    
    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_cancel(self):
        for activity in self:
            activity.registrations.action_cancel()
            activity.state = 'cancelled'


class ActivityRegistration(models.Model):
    _name = 'resource.activity.registration'
    
    def _get_activity_booking_type(self):
        if self.resource_activity_id.booking_type:
            self.booking_type = self.resource_activity_id.booking_type

    def _get_activity_activity_date_lock(self):
        if self.resource_activity_id.booking_type:
            self.booking_type = self.resource_activity_id.booking_type
        
    resource_activity_id = fields.Many2one('resource.activity',string="Activity")
    attendee_id = fields.Many2one('res.partner', string="Attendee", domain=[('customer','=',True)])
    quantity = fields.Integer(string="Quantity needed", default=1)
    quantity_allocated = fields.Integer(string="Quantity allocated", readonly=True)
    resource_category = fields.Many2one('resource.category', string="Category", required=True)
    resources_available = fields.One2many('resource.available','registration_id',string="Resource available")
    allocations = fields.One2many('resource.allocation', 'activity_registration_id',
                                  string="Activity registration")
    date_lock = fields.Date(string="Date lock", default=_get_activity_activity_date_lock)
    booking_type = fields.Selection([('option','Option'),
                                    ('booked','Booking')], string="Booking type", default=_get_activity_booking_type)
    state = fields.Selection([('draft','Draft'),
                              ('waiting','Waiting'),
                              ('available','Available'),
                              ('option','Option'),
                              ('booked','Booked'),
                              ('cancelled','Cancelled')],
                             string="State", default='draft', readonly=True)
    date_start = fields.Datetime(related='resource_activity_id.date_start', string="Date start")
    date_end = fields.Datetime(related='resource_activity_id.date_end', string="Date end")
    location_id = fields.Many2one(related='resource_activity_id.location_id', string="Location")


    def create_resource_available(self, resource_ids, registration):
        for resource_id in resource_ids:
            self.env['resource.available'].create({'resource_id':resource_id,
                                                  'registration_id':registration.id,
                                                  'state':'free'})

    
    @api.multi
    def search_resources(self):
        registrations = self.filtered(lambda record: record.state in ['draft','waiting'])
        for registration in registrations:
            if registration.quantity_allocated < registration.quantity:
                # delete free and unfree resource when running.
                res_to_delete = registration.resources_available.filtered(lambda record: record.state in ['free','not_free'])
                res_to_delete.unlink()
                if registration.resource_category: 
                    # we complete with the group resources
                    cat_resource_ids = registration.resource_category.resources.check_availabilities(registration.date_start, registration.date_end, registration.location_id)
                    self.create_resource_available(cat_resource_ids, registration)
                    
                    if len(registration.resources_available) >= registration.quantity:
                        registration.state = 'available'

        return True

    @api.multi
    def action_refresh(self):
        for registration in self:
            resources_available = registration.resources_available.filtered(lambda record: record.state == 'free')
            still_avai_res = resources_available.mapped('resource_id').check_availabilities(registration.date_start, registration.date_end, registration.location_id)
            for resource_available in resources_available:
                if resource_available.resource_id.id not in still_avai_res:
                    resource_available.state = 'not_free'
        return True

    @api.multi
    def action_cancel(self):
        for registration in self:
            for resource_available in registration.resources_available:
                resource_available.action_cancel()
            registration.state = 'cancelled'

    @api.multi
    @api.depends('quantity','quantity_allocated')
    def compute_state(self):
        for subscription in self:
            if self.quantity_allocated == self.quantity:
                self.state = self.booking_type
            elif self.quantity_allocated < self.quantity:
                self.state= 'waiting'

    @api.multi
    def view_registration_form(self):
        context = dict(self.env.context or {})
        context['active_id'] = self.id

        return {
            'name': 'view activity registration',
            'res_model': 'resource.activity.registration',
            'view_id': self.env.ref('resource_activity.view_activity_registration_form', False).id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': context,
        }


class ResourceAvailable(models.Model):
    _name = 'resource.available'

    name = fields.Char(related='resource_id.serial_number',string='Name')
    resource_id = fields.Many2one('resource.resource', string="Resource", required=True)
    registration_id = fields.Many2one('resource.activity.registration', string="Registration")
    state = fields.Selection([('free','Free'),
                              ('not_free','Not free'),
                              ('selected','Selected'),
                              ('cancelled','Cancelled')], string="State", readonly=True)

    @api.multi
    def action_reserve(self):
        allocation_ids = self.resource_id.allocate_resource(self.registration_id.booking_type,
                                                            self.registration_id.date_start,
                                                            self.registration_id.date_end,
                                                            self.registration_id.attendee_id,
                                                            self.registration_id.location_id,
                                                            self.registration_id.date_lock)
        if allocation_ids:
            allocations = self.env['resource.allocation'].browse(allocation_ids)
            allocations.write({'activity_registration_id': self.registration_id.id})
            self.registration_id.quantity_allocated += 1
            self.state = 'selected'
        else:
            print "no resource found for : " + str(self.resource_id.ids)

        return True

    @api.multi
    def action_cancel(self):
        allocation = self.registration_id.allocations.filtered(lambda record: record.resource_id.id == self.resource_id.id)
        allocation.action_cancel()
        self.registration_id.quantity_allocated -= 1
        self.state = 'cancelled'

