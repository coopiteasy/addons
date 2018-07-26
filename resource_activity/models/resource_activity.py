# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import pytz
from openerp import _, api, fields, models
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from openerp.exceptions import ValidationError, UserError


def _pd(dt):
    """parse datetime"""
    return datetime.strptime(dt, DTF) if dt else dt


class ResourceActivityType(models.Model):
    _name = 'resource.activity.type'

    name = fields.Char(string="Type", required=True)
    code = fields.Char(string="Code")
    analytic_account = fields.Many2one('account.analytic.account', string="Analytic account", groups="analytic.group_analytic_accounting")
    product_ids = fields.Many2many('product.product', string="Product")


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

    @api.multi
    @api.depends('registrations.need_push')
    def _compute_push2sale_order(self):
        # computed field in order to display or not the push to sale order button
        for activity in self:
            flag = False
            if activity.sale_order_id or activity.sale_orders:
                registrations = activity.registrations.filtered(lambda record: record.need_push == True)
                if registrations:
                    flag = True

            activity.need_push = flag

    @api.multi
    def _compute_booked_resources(self):
        for activity in self:
            booked_resources = []
            for registration in activity.registrations:
                res_ids = registration.allocations.filtered(lambda record: record.state in ['option','booked']).mapped('resource_id').ids
                if res_ids:
                    booked_resources = booked_resources + res_ids
            activity.booked_resources = booked_resources

    @api.multi
    def _compute_sale_orders(self):
        for activity in self:
            activity.sale_orders = activity.registrations.mapped('sale_order_id').ids

    name = fields.Char(string="Name", copy=False)
    partner_id = fields.Many2one('res.partner', string="Customer", domain=[('customer','=',True)])
    delivery_product_id = fields.Many2one('product.product', string="Product delivery", domain=[('is_delivery','=',True)])
    guide_product_id = fields.Many2one('product.product', string="Product Guide", domain=[('is_guide','=',True)])
    participation_product_id = fields.Many2one('product.product',
                                               string="Product Participation",
                                               domain=[('is_participation', '=', True)])
    date_start = fields.Datetime(string="Date start", required=True)
    date_end = fields.Datetime(string="Date end", required=True)
    duration = fields.Char(string="Duration", compute="_compute_duration", store=True)
    registrations = fields.One2many('resource.activity.registration', 'resource_activity_id', string="Registration")
    location_id = fields.Many2one('resource.location', string="Location", required=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale order", readonly=True, copy=False)
    state = fields.Selection([('draft','Draft'),
                              ('quotation','Quotation'),
                              ('sale','Sale'),
                              ('done','Done'),
                              ('cancelled','Cancelled')], string="State", default='draft')
    date_lock = fields.Date(string="Date lock")
    booking_type = fields.Selection([('option','Option'),
                                    ('booked','Booking')], string="Booking type", required=True, default='booked')
    active = fields.Boolean('Active', default=True)
    departure = fields.Char(string="Departure")
    arrival = fields.Char(string="Arrival")
    description = fields.Char(string="Description")
    comment = fields.Text(string="Comment")
    activity_type = fields.Many2one('resource.activity.type', string="Activity type", required=True)
    analytic_account = fields.Many2one(related='activity_type.analytic_account', string="Analytic account", readonly=True, groups="analytic.group_analytic_accounting")
    guides = fields.Many2many('res.partner',
                              relation='activity_guide',
                              column1='activity_id',
                              column2='guide_id',
                              string="Guide", domain=[('is_guide','=',True)])
    trainers = fields.Many2many('res.partner',
                                relation='activity_trainer',
                                column1='activity_id',
                                column2='trainer_id',
                                string="Trainer", domain=[('is_trainer','=',True)])
    langs = fields.Many2many('resource.activity.lang', string="Langs")
    activity_theme = fields.Many2one('resource.activity.theme', string="Activity theme")
    need_participation = fields.Boolean(string="Need participation?")
    need_delivery = fields.Boolean(string="Need delivery?")
    delivery_place = fields.Char(string="Delivery place")
    delivery_time = fields.Datetime(string="Delivery time")
    pickup_place = fields.Char(string="Pick up place")
    pickup_time = fields.Datetime(string="Pick up time")
    set_allocation_span = fields.Boolean(string='Set Allocation Span Manually', default=False)
    resource_allocation_start = fields.Datetime(string='Resource Allocation Start')
    resource_allocation_end = fields.Datetime(string='Resource Allocation End')
    need_guide = fields.Boolean(string="Need guide?")
    registrations_max = fields.Integer(string="Maximum registration")
    registrations_min = fields.Integer(string="Minimum registration")
    registrations_expected = fields.Integer(string="Registrations made",
                        store=True, readonly=True, compute='_compute_registrations')
    without_resource_reg = fields.Integer(string="Registrations without resource",
                        store=True, readonly=True, compute='_compute_registrations')
    company_id = fields.Many2one('res.company', string='Company', required=True, 
                        change_default=True, readonly=True,
                        default=lambda self: self.env['res.company']._company_default_get())
    need_push = fields.Boolean(string="Need to push to sale order", compute='_compute_push2sale_order', store=True)
    booked_resources = fields.One2many('resource.resource', string="Booked resources", compute='_compute_booked_resources')
    sale_orders = fields.One2many('sale.order', string="Sale orders", compute='_compute_sale_orders')

    @api.onchange('location_id')
    def onchange_location_id(self):
        if self.location_id and self.location_id.address:
            self.departure = self.location_id.address._display_address(self.location_id.address)
            self.arrival = self.location_id.address._display_address(self.location_id.address)

    @api.onchange('booking_type')
    def onchange_booking_type(self):
        if self.booking_type == 'booked':
            self.date_lock = None

    def _localize(self, date):
        tz = pytz.timezone(self._context['tz']) if self._context['tz'] else pytz.utc
        return pytz.utc.localize(date).astimezone(tz)

    def trunc_day(self, datetime_):
        datetime_ = self._localize(_pd(datetime_))
        datetime_ = datetime_.replace(hour=0, minute=0, second=0, microsecond=0)
        return datetime_.astimezone(pytz.utc)

    @api.onchange('date_start', 'date_end',
                  'need_delivery', 'delivery_time', 'pickup_time',
                  'set_allocation_span')
    def default_allocation_span(self):
        # todo, view readonly
        # todo make sure it records date when manually set
        if self.date_start:
            if self.need_delivery:
                if self.set_allocation_span:
                    start = _pd(self.date_start) - timedelta(minutes=90)
                else:
                    # get utc, set it to local time midnight
                    # send it back as utc
                    start = self.delivery_time if self.delivery_time else self.date_start
                    start = self.trunc_day(start)
            else:
                start = _pd(self.date_start)
            self.resource_allocation_start = start.strftime(DTF)

        if self.date_end:
            if self.need_delivery:
                if self.set_allocation_span:
                    end = _pd(self.date_end) + timedelta(minutes=90)
                else:
                    end = self.pickup_time if self.pickup_time else self.date_end
                    end = self.trunc_day(end) + timedelta(days=1)
            else:
                end = _pd(self.date_end)
            self.resource_allocation_end = end.strftime(DTF)

    @api.one
    @api.constrains('date_start', 'date_end')
    def _check_date(self):
        if self.date_end < self.date_start:
            raise ValidationError("Date end can't be before date start: %s %s" % (self.date_start,self.date_end))

    @api.one
    @api.constrains('date_start', 'date_end',
                    'resource_allocation_start', 'resource_allocation_end',
                    'need_delivery', 'delivery_time', 'pickup_time')
    def _activity_fields_blocked_if_resource_booked(self):
        if self.booked_resources:
            raise ValidationError('You cannot modify activity dates, resource allocation dates or delivery '
                                  'information when a resource is already booked. You must either delete this '
                                  'activity and create a new one or release all booked resources for this activity.')

    @api.multi
    @api.depends('registrations_max', 'registrations.state', 'registrations.quantity')
    def _compute_registrations(self):
        for activity in self:
            expected = 0
            qty_without_resource = 0
            for registration in activity.registrations.filtered(lambda record: record.state != 'cancelled'):
                expected += registration.quantity
                qty_without_resource += registration.quantity - registration.quantity_needed
            activity.registrations_expected = expected
            activity.without_resource_reg = qty_without_resource

    @api.multi
    @api.depends('date_end', 'date_start')
    def _compute_duration(self):
        period = timedelta(days=1)
        period_time = timedelta(hours=24)

        for activity in self:
            if activity.date_start and activity.date_end and activity.date_start < activity.date_end:
                datetime_end = datetime.strptime(activity.date_end, DTF)
                datetime_start = datetime.strptime(activity.date_start, DTF)
                date_end = datetime_end.date()
                date_start = datetime_start.date()

                delta_time = datetime_end - datetime_start

                if date_end > date_start:
                    delta = date_end - date_start
                    if delta_time > period_time: 
                        delta += period
                    activity.duration = str(delta.days) + " day(s)"

                elif date_end == date_start:
                    activity.duration = str(delta_time.seconds / 3600) + " hour(s) " + str(delta_time.seconds % 3600 // 60) +" minute(s)" 

    @api.multi
    def search_all_resources(self):
        for activity in self:
            activity.registrations.search_resources()

    @api.multi
    def reserve_needed_resource(self):
        for activity in self:
            activity.registrations.reserve_needed_resource()

    @api.multi
    def action_done(self):
        self.state = 'done'          

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_cancel(self):
        action = self.env.ref('resource_activity.action_cancel_sale_order')
        for activity in self:
            activity.registrations.action_cancel()
            activity.state = 'cancelled'

            return {
                'name': action.name,
                'help': action.help,
                'type': action.type,
                'view_type': action.view_type,
                'view_mode': action.view_mode,
                'target': action.target,
                'context': self._context,
                'res_model': action.res_model,
            }

    def create_order_line(self, line_vals, order_id, product, qty):
        line_vals['order_id'] = order_id.id
        line_vals['product_id'] = product.id
        line_vals['product_uom_qty'] = qty
        line_vals['product_uom'] = product.uom_id.id
        line_id = self.env['sale.order.line'].create(line_vals)
        line_id.update_line()
        
        return line_id

    @api.multi
    def create_sale_order(self):
        order_obj = self.env['sale.order']
        for activity in self:
            order_vals = {
                'activity_id': activity.id,
                'project_id': activity.analytic_account.id,
                'activity_sale': True,
                }
            # if the whole activity is for the same customer we only create one sale order
            if activity.partner_id:
                order_vals['partner_id'] = activity.partner_id.id
                order_id = order_obj.create(order_vals)
                self.write({'sale_order_id': order_id.id, 'state':'quotation'})
            
            no_bike_qty = 0
            bike_qty = 0

            customers = {}
            for registration in activity.registrations.filtered(lambda record: record.state != 'cancelled'):
                if not activity.partner_id:
                    order_vals = {
                        'activity_id': activity.id,
                        'project_id': activity.analytic_account.id,
                        'activity_sale': True,
                    }
                    attendee_id = registration.attendee_id.id
                    if not customers.has_key(attendee_id):
                        order_vals['partner_id'] = attendee_id
                        order_id = order_obj.create(order_vals)
                        customers[attendee_id] = order_id
                    else:
                        order_id = customers[attendee_id]
                    registration.write({'sale_order_id': order_id.id})

                    if activity.need_delivery:
                        line_vals = {'resource_delivery': True}
                        line_id = self.create_order_line(line_vals, order_id, activity.delivery_product_id, registration.quantity_needed)
    
                    if activity.need_participation:
                        line_vals = {'participation_line': True}
                        line_id = self.create_order_line(line_vals, order_id, activity.participation_product_id, registration.quantity)

                no_bike_qty += registration.quantity - registration.quantity_needed
                bike_qty += registration.quantity_needed
                line_vals = {}
                line_id = self.create_order_line(line_vals, order_id, registration.product_id, registration.quantity_needed)
                registration.order_line_id = line_id

            if activity.partner_id:
                if activity.need_delivery:
                    line_vals = {'resource_delivery': True}
                    line_id = self.create_order_line(line_vals, order_id, activity.delivery_product_id, bike_qty)

                if activity.need_guide:
                    line_vals = {'resource_guide': True}
                    line_id = self.create_order_line(line_vals, order_id, activity.guide_product_id, len(activity.guides))

                if activity.need_participation:
                    line_vals = {'participation_line': True}
                    line_id = self.create_order_line(line_vals, order_id, activity.participation_product_id, activity.registrations_expected)

    @api.multi
    def action_quotation(self):
        for activity in self:
            if activity.sale_order_id:
                activity.sale_order_id.with_context(activity_action=True).action_cancel()
                activity.sale_order_id.with_context(activity_action=True).action_draft()
                activity.state = 'quotation'

    @api.multi
    def action_sale_order(self):
        res_acti_seq = self.env.ref('resource_activity.sequence_resource_activity', False)
        for activity in self:
            vals = {'booking_type':'booked'}
            if activity.name == '' or not activity.name:
                vals['name'] = res_acti_seq.next_by_id()

            if activity.sale_order_id:
                activity.sale_order_id.with_context(activity_action=True).action_confirm()
                vals['state'] = 'sale'

            activity.write(vals)

            options = activity.registrations.filtered(lambda record: record.booking_type in ['option'])
            for option in options:
                option.allocations.action_confirm()
                option.write({'booking_type':'booked','state':'booked','date_lock': None})

    @api.multi            
    def push_changes_2_sale_order(self):
        for activity in self:
            if activity.sale_order_id:
                bike_qty = 0
                # handling resource reservation here
                activity.sale_order_id.project_id = activity.analytic_account
                for registration in activity.registrations:
                    if registration.state != 'cancelled':
                        bike_qty += registration.quantity_needed

                    if registration.need_push:
                        line_vals = {}
                        self.update_order_line(activity.sale_order_id, True, line_vals, registration.order_line_id, registration.quantity_needed, registration.product_id)
                        registration.need_push = False

                # handling delivery here        
                delivery_line = activity.sale_order_id.order_line.filtered(lambda record: record.resource_delivery == True)
                line_vals = {'resource_delivery': True}

                self.update_order_line(activity.sale_order_id, activity.need_delivery, line_vals, delivery_line, bike_qty, activity.delivery_product_id)

                # handling guide here
                guide_line = activity.sale_order_id.order_line.filtered(lambda record: record.resource_guide == True)
                line_vals = {'resource_guide':True}
                guide_qty = len(activity.guides)

                self.update_order_line(activity.sale_order_id, activity.need_guide, line_vals, guide_line, guide_qty,  activity.guide_product_id)

                # handling participation here
                participation_line = activity.sale_order_id.order_line.filtered(lambda record: record.participation_line == True)
                line_vals = {'participation_line':True}
                self.update_order_line(activity.sale_order_id, activity.need_participation, line_vals, participation_line, activity.registrations_expected, activity.participation_product_id)
            elif activity.sale_orders:
                # if the activity is spread on several sale orders
                needed_res = {}
                participations = {}

                for registration in activity.registrations:
                    registration.sale_order_id.project_id = activity.analytic_account
                    attendee_id = registration.attendee_id.id
                    
                    if needed_res.has_key(attendee_id):
                        needed_res[attendee_id] += registration.quantity_needed
                        participations[attendee_id] += registration.quantity
                    else:
                        needed_res[attendee_id] = registration.quantity_needed
                        participations[attendee_id] = registration.quantity
                    if registration.need_push:
                        line_vals = {}
                        self.update_order_line(registration.sale_order_id, True, line_vals, registration.order_line_id, needed_res[attendee_id], registration.product_id)
                        registration.need_push = False

                    # handling delivery here        
                    delivery_line = registration.sale_order_id.order_line.filtered(lambda record: record.resource_delivery == True)
                    line_vals = {'resource_delivery': True}
    
                    self.update_order_line(registration.sale_order_id, activity.need_delivery, line_vals, delivery_line, needed_res[attendee_id], activity.delivery_product_id)

                    # handling participation here
                    participation_line = registration.sale_order_id.order_line.filtered(lambda record: record.participation_line == True)
                    line_vals = {'participation_line':True}
                    self.update_order_line(registration.sale_order_id, activity.need_participation, line_vals, participation_line, participations[attendee_id], activity.participation_product_id)

            activity.need_push = False

    def update_order_line(self, order_id, need_resource, line_vals, resource_line, resource_qty, resource_product_id):
        if need_resource:
            line_vals['product_uom_qty'] = resource_qty
            line_vals['product_id'] = resource_product_id.id
            if resource_line:
                resource_line.write(line_vals)
                resource_line.update_line()
            else:
                line_vals['order_id'] = order_id.id
                line_vals['product_uom'] = resource_product_id.uom_id.id
                self.env['sale.order.line'].create(line_vals)
        else:
            if resource_line:
                resource_line.unlink()

    @api.multi
    def write(self,vals):
        for activity in self:
            if activity.sale_order_id or activity.sale_orders:
                if 'need_delivery' in vals:
                    if not vals.get('need_delivery'):
                        vals['delivery_place'] = ''
                        vals['delivery_time'] = False
                        vals['pickup_place'] = ''
                        vals['pickup_time'] = False
                        vals['delivery_product_id'] = False
                    vals['need_push'] = True
                if 'need_guide' in vals:
                    if not vals.get('need_guide'):
                        vals['guide_product_id'] = False
                    vals['need_push'] = True
                if 'need_participation' in vals:
                    if not vals.get('need_participation'):
                        vals['need_participation'] = False
                    vals['need_push'] = True
                if 'activity_type' in vals:
                    vals['need_push'] = True
        return super(ResourceActivity,self).write(vals)

    @api.multi
    @api.depends('partner_id', 'registrations_max','registrations_expected')
    def _propagate_activity_fields_update(self):
        for activity in self:
            vals = {}
            vals['partner_id'] = activity.partner_id
            vals['registrations_max'] = activity.registrations_max
            vals['registrations_expected'] = activity.registrations_expected
            activity.registrations.write(vals)


class ActivityRegistration(models.Model):
    _name = 'resource.activity.registration'

    def _get_activity_booking_type(self):
        if self.resource_activity_id.booking_type:
            self.booking_type = self.resource_activity_id.booking_type
 
    def _get_activity_activity_date_lock(self):
        if self.resource_activity_id.booking_type:
            self.booking_type = self.resource_activity_id.booking_type

    @api.onchange('resource_category')
    def onchange_resource_category(self):
        self.product_id = False

    @api.onchange('quantity')
    def onchange_quantity(self):
        if not self.bring_bike and self.state not in ['option','booked']:
            self.quantity_needed = self.quantity

    @api.onchange('quantity_needed')
    def onchange_quantity_needed(self):
        if self.state not in ['booked','option','draft']:
            if self.quantity_needed > self.quantity_allocated:
                self.state= 'waiting'

    @api.onchange('bring_bike')
    def onchange_bring_bike(self):
        if self.bring_bike:
            self.quantity_needed = 0
        else:
            self.quantity_needed = self.quantity

    @api.onchange('booking_type')
    def onchange_booking_type(self):
        if self.booking_type == 'booked':
            self.date_lock = None

    @api.multi
    @api.depends('quantity_needed', 'product_id','state')
    def _compute_need_push(self):
        for registration in self:
            if registration.resource_activity_id.sale_order_id or registration.sale_order_id:
                registration.need_push = True

    resource_activity_id = fields.Many2one('resource.activity',string="Activity")
    order_line_id = fields.Many2one('sale.order.line', string="Sale order line")
    partner_id = fields.Many2one(related='resource_activity_id.partner_id')
    attendee_id = fields.Many2one('res.partner', string="Attendee", domain=[('customer','=',True)])
    sale_order_id = fields.Many2one('sale.order', string="Sale order", readonly=True, copy=False)
    quantity = fields.Integer(string="Number of participant", default=1)
    quantity_needed = fields.Integer(string="Quantity needed", default=1)
    quantity_allocated = fields.Integer(string="Quantity allocated", readonly=True)
    product_id = fields.Many2one('product.product', string="Product")
    resource_category = fields.Many2one('resource.category', string="Category")
    resources_available = fields.One2many('resource.available','registration_id',string="Resource available")
    allocations = fields.One2many('resource.allocation', 'activity_registration_id',
                                  string="Activity registration")
    date_lock = fields.Date(string="Date lock")
    booking_type = fields.Selection([('option','Option'),
                                      ('booked','Booking')],string="Booking type", required=True)
    state = fields.Selection([('draft','Draft'),
                              ('waiting','Waiting'),
                              ('available','Available'),
                              ('option','Option'),
                              ('booked','Booked'),
                              ('cancelled','Cancelled')],
                             string="State", default='draft', readonly=True)
    # depends of the resource type
    date_start = fields.Datetime(related='resource_activity_id.resource_allocation_start', string="Date start")
    date_end = fields.Datetime(related='resource_activity_id.resource_allocation_end', string="Date end")
    location_id = fields.Many2one(related='resource_activity_id.location_id', string="Location")
    bring_bike = fields.Boolean(string="Bring his bike")
    registrations_max = fields.Integer(string="Maximum registration")
    registrations_expected = fields.Integer(string="Expected registration")
    activity_type = fields.Many2one('resource.activity.type', string="Activity type")
    need_push = fields.Boolean(string="Need to be pushed to sales order", compute='_compute_need_push', store=True)

    def create_resource_available(self, resource_ids, registration):
        for resource_id in resource_ids:
            self.env['resource.available'].create({'resource_id':resource_id,
                                                  'registration_id':registration.id,
                                                  'state':'free'})

    @api.multi
    def search_resources(self):
        registrations = self.filtered(lambda record: record.state in ['draft','waiting','available'])
        for registration in registrations:
            if registration.quantity_allocated < registration.quantity_needed:
                # delete free and unfree resource when running.
                res_to_delete = registration.resources_available.filtered(lambda record: record.state in ['free','not_free'])
                res_to_delete.unlink()
                if registration.resource_category: 
                    # we complete with the group resources
                    cat_resource_ids = (
                        registration
                        .resource_category
                        .resources
                        .check_availabilities(registration.date_start,
                                              registration.date_end,
                                              registration.location_id)
                    )
                    self.create_resource_available(cat_resource_ids, registration)
                    
                    if len(registration.resources_available.filtered(lambda record: record.state != 'cancelled')) >= registration.quantity_needed:
                        registration.state = 'available'
                    else:
                        registration.state = 'waiting'
                        self.env.cr.commit()
                        raise UserError(("Not enough resource found for the registration %s with category %s. %s resources found") % 
                                            (registration.attendee_id.name, registration.resource_category.name, len(registration.resources_available)))

        return True

    @api.multi
    def action_refresh(self):
        for registration in self:
            resources_available = (
                registration
                .resources_available
                .filtered(lambda record: record.state == 'free')
            )
            still_avai_res = (
                resources_available
                .mapped('resource_id')
                .check_availabilities(registration.date_start,
                                      registration.date_end,
                                      registration.location_id)
            )
            for resource_available in resources_available:
                if resource_available.resource_id.id not in still_avai_res:
                    resource_available.state = 'not_free'
        return True

    @api.multi
    def reserve_needed_resource(self):
        for registration in self:
            qty_needed = registration.quantity_needed - registration.quantity_allocated
            free_resources = (
                registration
                .resources_available
                .filtered(lambda record: record.state == 'free')
            )
            for resource_available in free_resources:
                resource_available.action_reserve()
                qty_needed -= 1
                if qty_needed == 0:
                    break
            (registration
             .resource_activity_id
             .registrations.action_refresh())
        return True

    @api.multi
    def action_cancel(self):
        for registration in self:
            for resource_available in registration.resources_available:
                resource_available.action_cancel()
            registration.write({'state':'cancelled','quantity_allocated':0})

    @api.multi
    def action_draft(self):
        self.write({'state':'draft'})

    @api.multi
    def action_unlink(self):
        self.unlink()

    @api.multi
    def unlink(self):
        for registration in self:
            if registration.state not in ('draft', 'cancelled', 'free'):
                raise UserError(_('You cannot delete a registration which is not draft or cancelled. You should first cancel it.'))
        return super(ActivityRegistration, self).unlink()

    @api.multi
    @api.depends('quantity','quantity_allocated')
    def compute_state(self):
        for subscription in self:
            if self.quantity_allocated == self.quantity:
                self.state = self.booking_type
            elif self.state != 'draft' and self.quantity_allocated < self.quantity:
                self.state= 'waiting'

    @api.multi
    def view_registration_form(self):
        self.action_refresh()
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

    @api.model
    def create(self,vals):
        if vals.get('registrations_max') > 0 and vals.get('registrations_max') < vals.get('registrations_expected') + vals.get('quantity_needed'):
            raise ValidationError("Maximum registration capacity reached")
        return super(ActivityRegistration,self).create(vals)

    @api.multi
    def write(self,vals):
        for registration in self:
            if registration.registrations_max \
                    and vals.get('quantity') \
                    and registration.registrations_max < (registration.registrations_expected
                                - registration.quantity
                                + vals.get('quantity')):
                raise ValidationError("Maximum registration capacity reached")
        return super(ActivityRegistration,self).write(vals)


class ResourceAvailable(models.Model):
    _name = 'resource.available'

    name = fields.Char(related='resource_id.serial_number',string='Name')
    resource_id = fields.Many2one('resource.resource', string="Resource", required=True)
    registration_id = fields.Many2one('resource.activity.registration', string="Registration")
    activity_id = fields.Many2one(related='registration_id.resource_activity_id', string="Activity", readonly=True)
    state = fields.Selection([('free','Free'),
                              ('not_free','Not free'),
                              ('selected','Selected'),
                              ('cancelled','Cancelled')], string="State", readonly=True)

    @api.multi
    def action_reserve(self):
        for resource_available in self.filtered(lambda record: record.state == 'free'):
            allocation_ids = (
                resource_available
                .resource_id
                .allocate_resource(resource_available.registration_id.booking_type,
                                   resource_available.registration_id.date_start,
                                   resource_available.registration_id.date_end,
                                   resource_available.registration_id.attendee_id,
                                   resource_available.registration_id.location_id,
                                   resource_available.registration_id.date_lock)
            )
            if allocation_ids:
                allocations = self.env['resource.allocation'].browse(allocation_ids)
                allocations.write({'activity_registration_id': resource_available.registration_id.id})
                resource_available.state = 'selected'
                resource_available.registration_id.quantity_allocated += 1
                resource_available.registration_id.state = resource_available.registration_id.booking_type
            else:
                print "no resource found for : " + str(resource_available.resource_id.ids)
            self.activity_id.registrations.action_refresh()
        return True

    @api.multi
    def action_cancel(self):
        allocation = self.registration_id.allocations.filtered(lambda record: record.resource_id.id == self.resource_id.id and record.state != 'cancel')
        allocation.action_cancel()
        if self.state == 'selected':
            self.registration_id.quantity_allocated -= 1
            if self.registration_id.quantity_needed > self.registration_id.quantity_allocated \
                and self.registration_id.quantity_allocated > 0:
                self.registration_id.state = 'waiting'
            elif self.registration_id.quantity_allocated == 0:
                self.registration_id.state = 'cancelled'
        self.state = 'cancelled'

        return True

