# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResourceAllocation(models.Model):
    _inherit = 'resource.allocation'
    
    activity_registration_id = fields.Many2one('resource.activity.registration', string="Activity registration")

class ResourceActivity(models.Model):
    _name = 'resource.activity'

    _inherit = ['mail.thread']
    
    name = fields.Char(string="Name")
    date_start = fields.Datetime(string="Date start", required=True)
    date_end = fields.Datetime(string="Date end", required=True)
    registrations = fields.One2many('resource.activity.registration', 'resource_activity_id', string="Registration")
    location_id = fields.Many2one('resource.location', string="Location", required=True)
    state = fields.Selection([('draft','Draft'),
                              ('confirmed','Confirmed'),
                              ('done','Done'),
                              ('cancel','cancel')], string="State", default='draft')
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
        self.state = 'cancelled'


class ActivityRegistration(models.Model):
    _name = 'resource.activity.registration'
    
    resource_activity_id = fields.Many2one('resource.activity',string="Activity")
    attendee_id = fields.Many2one('res.partner', string="Attendee")
    resources = fields.Many2many('resource.resource')
    allocations = fields.One2many('resource.allocation', 'activity_registration_id',
                                  string="Activity registration")
    date_lock = fields.Date(string="Date lock")
    booking_type = fields.Selection([('option','Option'),
                                    ('booked','Booked')], string="Booking type", default='option')
    state = fields.Selection([('draft','Draft'),
                              ('waiting','Waiting'),
                              ('booked','Booked'),
                              ('option','Option'),
                              ('cancelled','Cancelled')], 
                             string="State", default='draft')

    @api.multi
    def action_allocate(self):
        registrations = self.filtered(lambda record: record.state in ['draft','waiting'])
        if registrations:
            date_start = registrations[0].resource_activity_id.date_start
            date_end = registrations[0].resource_activity_id.date_end
            location_id = registrations[0].resource_activity_id.location_id
        for registration in registrations:
            resource_ids = registration.resources.check_availabilities(date_start, date_end, location_id)
            allocation_ids = registration.resources.allocate_resource(registration.booking_type, date_start, date_end, registration.attendee_id, location_id, registration.date_lock)
            allocations = self.env['resource.allocation'].browse(allocation_ids)
            allocations.write({'activity_registration_id':registration.id})
            if set(registration.resources.ids).issubset(resource_ids):
                registration.state = registration.booking_type
            else:
                diff = list(set(registration.resources.ids).symmetric_difference(set(resource_ids)))
                print "no resource found for : " + str(diff) 
                registration.state = "waiting"


    @api.multi
    def action_option(self):
        self.state = 'option'

    @api.multi
    def action_book(self):
        self.state = 'booked'

    @api.multi
    def action_cancel(self):
        self.state = 'cancelled'
