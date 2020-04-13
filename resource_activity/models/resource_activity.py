# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from collections import defaultdict, namedtuple

import pytz
from openerp import _, api, fields, models
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from openerp.exceptions import ValidationError, UserError

OrderLine = namedtuple('OrderLine',
                       ['partner', 'product', 'qty', 'type', 'registration'])


def _pd(dt):
    """parse datetime"""
    return datetime.strptime(dt, DTF) if dt else dt


class ResourceActivityDelivery(models.Model):
    _name = 'resource.activity.delivery'

    activity_id = fields.Many2one(
        'resource.activity',
        string="Activity",
        required=True,
        ondelete='cascade',
    )
    activity_description = fields.Char(
        related='activity_id.description',
        string="Description",
    )
    activity_type = fields.Many2one(
        'resource.activity.type',
        string="Activity type",
        related='activity_id.activity_type',
    )
    location_id = fields.Many2one(
        'resource.location',
        string="Location",
        related='activity_id.location_id',
    )
    delivery_type = fields.Selection(
        [
            ('delivery', 'Delivery'),
            ('pickup', 'Pick up'),
        ],
        string="Type",
        required=True,
    )
    nb_allocated_resources = fields.Integer(
        string="Allocated Resources",
        related='activity_id.nb_allocated_resources',
    )
    state = fields.Selection(
        related='activity_id.state',
        string="State",
    )
    date = fields.Datetime(
        string="Date",
        compute='_compute_date',
        store=True,
    )
    place = fields.Char(
        string="Place",
        compute='_compute_place',
    )

    @api.multi
    @api.depends('activity_id.delivery_time', 'activity_id.pickup_time')
    def _compute_date(self):
        for delivery in self:
            if delivery.is_delivery():
                delivery.date = delivery.activity_id.delivery_time
            elif delivery.is_pickup():
                delivery.date = delivery.activity_id.pickup_time
            else:
                raise ValueError(_("'delivery_type' is not defined"))

    @api.multi
    @api.depends('activity_id.delivery_place', 'activity_id.pickup_place')
    def _compute_place(self):
        for delivery in self:
            if delivery.is_delivery():
                delivery.place = delivery.activity_id.delivery_place
            elif delivery.is_pickup():
                delivery.place = delivery.activity_id.pickup_place
            else:
                raise ValueError(_("'delivery_type' is not defined"))

    def is_delivery(self):
        self.ensure_one()
        return self.delivery_type == 'delivery'

    def is_pickup(self):
        self.ensure_one()
        return self.delivery_type == 'pickup'


class ResourceActivityType(models.Model):
    _name = 'resource.activity.type'

    name = fields.Char(
        string="Type",
        required=True,
        translate=True,
    )
    code = fields.Char(
        string="Code")
    analytic_account = fields.Many2one(
        'account.analytic.account',
        string="Analytic account",
        groups="analytic.group_analytic_accounting")
    product_ids = fields.Many2many(
        'product.product',
        string="Product")
    active = fields.Boolean('Active', default=True)
    terms_conditions_id = fields.Many2one(
        comodel_name="res.company.terms",
        string="Terms and Conditions",
        help="Terms and Conditions related to this activity type"
    )


class ResourceActivityTheme(models.Model):
    _name = 'resource.activity.theme'

    name = fields.Char(
        string="Type",
        required=True,
        translate=True,
    )
    code = fields.Char(string="Code")
    active = fields.Boolean('Active', default=True)


class ResourceActivityLang(models.Model):
    _name = 'resource.activity.lang'

    name = fields.Char(
        string="Lang",
        required=True,
        translate=True,
    )
    code = fields.Char(
        string="Code")
    active = fields.Boolean('Active', default=True)


class ResourceActivity(models.Model):
    _name = 'resource.activity'
    _inherit = ['mail.thread']
    _order = 'date_start'

    @api.multi
    @api.depends('registrations.need_push')
    def _compute_push2sale_order(self):
        # computed field in order to display or not the push to sale order
        # button
        for activity in self:
            if activity.sale_orders:
                registrations_need_push = any(
                    activity
                    .registrations
                    .mapped('need_push'))
                activity.need_push = activity.need_push or registrations_need_push
        return

    @api.multi
    def _compute_booked_resources(self):
        for activity in self:
            booked_resources = []
            for registration in activity.registrations:
                res_ids = (
                    registration
                    .allocations
                    .filtered(
                        lambda record: record.state in ['option', 'booked'])
                    .mapped('resource_id')
                    .ids
                )
                if res_ids:
                    booked_resources = booked_resources + res_ids
            activity.booked_resources = booked_resources

    @api.multi
    def _compute_sale_orders(self):
        for activity in self:
            activity.sale_orders = (
                self.env['sale.order']
                    .search([('activity_id', '=', activity.id)])
                    .ids
            )

    @api.multi
    @api.depends('registrations.is_paid',
                 'registrations.state',
                 'state',
                 )
    def _compute_registrations_paid(self):
        for activity in self:
            if activity.state in ('sale', 'done'):
                registrations = (
                    activity
                    .registrations
                    .filtered(lambda record: record.state == 'booked')
                )

                activity.registrations_paid = all(
                    registrations.mapped('is_paid')
                )
            else:
                activity.registrations_paid = False

    @api.model
    def init_payments_fields(self):
        activities = self.search([])
        activities._compute_registrations_paid()
        return

    def _default_location(self):
        location = self.env.user.resource_location
        if location:
            return location
        else:
            raise UserError(_('No location set for current user'))

    name = fields.Char(
        string="Name",
        copy=False)
    partner_id = fields.Many2one(
        'res.partner',
        string="Customer",
        domain=[('customer', '=', True)])
    delivery_product_id = fields.Many2one(
        'product.product',
        string="Product delivery",
        domain=[('is_delivery', '=', True)])
    guide_product_id = fields.Many2one(
        'product.product',
        string="Product Guide",
        domain=[('is_guide', '=', True)])
    participation_product_id = fields.Many2one(
        'product.product',
        string="Product Participation",
        domain=[('is_participation', '=', True)])
    date_start = fields.Datetime(
        string="Date start",
        required=True)
    date_end = fields.Datetime(
        string="Date end",
        required=True)
    duration = fields.Char(
        string="Duration",
        compute="_compute_duration",
        store=True)
    registrations = fields.One2many(
        'resource.activity.registration',
        'resource_activity_id',
        string="Registration")
    location_id = fields.Many2one(
        'resource.location',
        string="Location",
        required=True,
        default=_default_location
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('quotation', 'Quotation'),
         ('sale', 'Sale'),
         ('done', 'Done'),
         ('cancelled', 'Cancelled')],
        string="State",
        default='draft')
    date_lock = fields.Date(
        string="Date lock")
    booking_type = fields.Selection(
        [('option', 'Option'),
         ('booked', 'Booking')],
        string="Booking type",
        required=True,
        default='booked')
    active = fields.Boolean(
        'Active',
        default=True)
    departure = fields.Char(
        string="Departure")
    arrival = fields.Char(
        string="Arrival")
    description = fields.Char(
        string="Description")
    comment = fields.Html(
        string="Comment")
    activity_type = fields.Many2one(
        'resource.activity.type',
        string="Activity type",
        required=True)
    analytic_account = fields.Many2one(
        related='activity_type.analytic_account',
        string="Analytic account",
        readonly=True,
        groups="analytic.group_analytic_accounting")
    guides = fields.Many2many(
        'res.partner',
        relation='activity_guide',
        column1='activity_id',
        column2='guide_id',
        string="Guide",
        domain=[('is_guide', '=', True)])
    trainers = fields.Many2many(
        'res.partner',
        relation='activity_trainer',
        column1='activity_id',
        column2='trainer_id',
        string="Trainer",
        domain=[('is_trainer', '=', True)])
    langs = fields.Many2many(
        'resource.activity.lang',
        string="Langs")
    activity_theme = fields.Many2one(
        'resource.activity.theme',
        string="Activity theme")
    need_participation = fields.Boolean(
        string="Need participation?")
    need_delivery = fields.Boolean(
        string="Need delivery?")
    delivery_ids = fields.One2many(
        'resource.activity.delivery',
        'activity_id',
        string="Delivery",
        ondelete='set null')
    delivery_place = fields.Char(
        string="Delivery place")
    delivery_time = fields.Datetime(
        string="Delivery time")
    pickup_place = fields.Char(
        string="Pick up place")
    pickup_time = fields.Datetime(
        string="Pick up time")
    set_allocation_span = fields.Boolean(
        string='Set Allocation Span Manually',
        default=False)
    resource_allocation_start = fields.Datetime(
        string='Resource Allocation Start')
    resource_allocation_end = fields.Datetime(
        string='Resource Allocation End')
    need_guide = fields.Boolean(
        string="Need guide?")
    registrations_max = fields.Integer(
        string="Maximum registration")
    registrations_min = fields.Integer(
        string="Minimum registration")
    registrations_expected = fields.Integer(
        string="Registrations made",
        store=True,
        readonly=True,
        compute='_compute_registrations')
    nb_allocated_resources = fields.Integer(
        string="Allocated Resources",
        compute='_compute_registrations',
    )
    without_resource_reg = fields.Integer(
        string="Registrations without resource",
        store=True,
        readonly=True,
        compute='_compute_registrations')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        change_default=True,
        readonly=True,
        default=lambda self: self.env['res.company']._company_default_get())
    need_push = fields.Boolean(
        string="Need to push to sale order",
        compute='_compute_push2sale_order',
        store=True)
    booked_resources = fields.One2many(
        'resource.resource',
        string="Booked resources",
        compute='_compute_booked_resources')
    sale_orders = fields.One2many(
        'sale.order',
        string="Sale orders",
        compute='_compute_sale_orders')
    registrations_paid = fields.Boolean(
        string='All Registrations Paid',
        compute='_compute_registrations_paid',
        store=True,
    )
    is_start_outside_opening_hours = fields.Boolean(
        string='Activity start is outside opening hours',
        compute='_compute_outside_opening_hours',
    )
    is_end_outside_opening_hours = fields.Boolean(
        string='Activity end is outside opening hours',
        compute='_compute_outside_opening_hours',
    )

    @api.multi
    @api.depends('date_end', 'date_start')
    def _compute_outside_opening_hours(self):
        opening_hours = self.env['activity.opening.hours']
        for activity in self:
            if activity.date_start and activity.date_end:
                activity.is_start_outside_opening_hours = not (
                    opening_hours.is_location_open(activity.location_id,
                                                   activity.date_start)
                )
                activity.is_end_outside_opening_hours = not (
                    opening_hours.is_location_open(activity.location_id,
                                                   activity.date_end)
                )

    @api.onchange('location_id')
    def onchange_location_id(self):
        if self.location_id and self.location_id.address:
            self.departure = (
                self.location_id
                    .address
                    ._display_address(self.location_id.address)
            )
            self.arrival = (
                self.location_id
                    .address
                    ._display_address(self.location_id.address)
            )

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
            raise ValidationError(_("Date end can't be before date start:"))

    @api.one
    @api.constrains('date_start', 'date_end',
                    'resource_allocation_start', 'resource_allocation_end',
                    'need_delivery', 'delivery_time', 'pickup_time')
    def _activity_fields_blocked_if_resource_booked(self):
        if self.booked_resources:
            raise ValidationError(_(
                'You cannot modify activity dates, resource allocation dates '
                'or delivery information when a resource is already booked. '
                'You must either delete this activity and create a new one or '
                'release all booked resources for this activity.'))

    @api.multi
    @api.depends('registrations_max',
                 'registrations.state',
                 'registrations.quantity')
    def _compute_registrations(self):
        for activity in self:
            registrations = (
                activity
                .registrations
                .filtered(lambda record: record.state != 'cancelled')
            )

            activity.registrations_expected = sum(
                registrations.mapped('quantity')
            )
            activity.without_resource_reg = sum(
                map(lambda reg: reg.quantity - reg.quantity_needed, registrations)
            )
            activity.nb_allocated_resources = sum(
                registrations.mapped('quantity_allocated')
            )

    @api.multi
    @api.depends('date_end', 'date_start')
    def _compute_duration(self):
        period = timedelta(days=1)
        period_time = timedelta(hours=24)

        for activity in self:
            if (activity.date_start
                    and activity.date_end
                    and activity.date_start < activity.date_end):

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
                    activity.duration = (
                            str(delta_time.seconds / 3600)
                            + " hour(s) "
                            + str(delta_time.seconds % 3600 // 60)
                            + " minute(s)"
                    )


    @api.multi
    def search_all_resources(self):
        for activity in self:
            activity.registrations.search_resources()

    @api.multi
    def reserve_needed_resource(self):
        for activity in self:
            activity.registrations.reserve_needed_resource()

    @api.multi
    def unreserve_resources(self):
        registrations = self.env['resource.activity.registration'].browse()
        for activity in self:
            for registration in activity.registrations:
                if registration.state == "booked":
                    registrations |= registration
        registrations.action_cancel()
        registrations.action_draft()

    @api.multi
    def mark_all_as_paid(self):
        for activity in self:
            activity.registrations.mark_as_paid()

    @api.multi
    def action_done(self):
        """
        Allowed from
        - sale state
        - draft state if nothing to invoice
        - allow bur warn from draft state with invoiced resources
        """
        for activity in self:
            registrations = (
                activity
                .registrations
                .filtered(lambda r: r.state in ['option', 'booked'])
            )
            # warn if in draft and invoiced resources booked
            if (activity.state == 'draft'
                and (registrations or activity.guides or activity.trainers)):
                action = self.env.ref(
                    'resource_activity.action_draft_to_done')
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
            elif activity.state in ('draft', 'sale'):
                activity.state = 'done'

    @api.multi
    def action_draft(self):
        for activity in self:
            activity.state = 'draft'

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

    def create_order_line(self, order, product, qty, **kwargs):
        line_values = {
            'order_id': order.id,
            'product_id': product.id,
            'product_uom_qty': qty,
            'product_uom': product.uom_id.id,

        }
        line_values.update(kwargs)
        line_id = self.env['sale.order.line'].create(line_values)
        line_id.update_line()
        return line_id

    def prepare_lines(self, activity):
        registrations = (
            activity
            .registrations
            .filtered(lambda record: record.state != 'cancelled')
        )
        prepared_lines = []
        for registration in registrations:
            if activity.partner_id:
                partner = activity.partner_id.id
            else:
                partner = registration.attendee_id.id

            if activity.need_delivery and registration.quantity_needed > 0:
                prepared_lines.append(
                    OrderLine(
                        partner,
                        activity.delivery_product_id,
                        registration.quantity_needed,
                        'delivery',
                        registration
                    )
                )
            if activity.need_participation:
                prepared_lines.append(
                    OrderLine(
                        partner,
                        activity.participation_product_id,
                        registration.quantity,
                        'participation',
                        registration
                    )
                )
            if registration.quantity_needed > 0:
                prepared_lines.append(
                    OrderLine(
                        partner,
                        registration.product_id,
                        registration.quantity_needed,
                        'resource',
                        registration
                    )
                )

        return prepared_lines

    def _create_sale_order(self, activity, partner_id):
        SaleOrder = self.env['sale.order']
        order_id = SaleOrder.create({
                    'partner_id': partner_id,
                    'activity_id': activity.id,
                    'project_id': activity.analytic_account.id,
                    'activity_sale': True,
        })
        activity.state = 'quotation'
        return order_id

    def prepare_sale_orders(self, activity):
        """
        create sale orders or get sale order ids and unlink sale order lines
        :param activity:
        :return:
        """
        registrations = (
            activity
            .registrations
            .filtered(lambda record: record.state != 'cancelled')
        )

        sale_orders = {}
        for registration in registrations:
            if activity.partner_id:
                partner = activity.partner_id.id
            else:
                partner = registration.attendee_id.id

            if partner not in sale_orders:
                if registration.sale_order_id and registration.sale_order_id.state != 'cancel':
                    sale_orders[partner] = registration.sale_order_id
                    for order_line in registration.sale_order_id.order_line:
                        order_line.unlink()
                else:
                    order_id = self._create_sale_order(activity, partner)
                    sale_orders[partner] = order_id

        return sale_orders

    @api.multi
    def create_sale_order(self):
        for activity in self:

            order_lines = self.prepare_lines(activity)
            if not order_lines:
                raise ValidationError(_('Nothing to invoice on this activity.'))

            sale_orders = self.prepare_sale_orders(activity)

            partners = set(ol.partner for ol in order_lines)
            for partner in partners:
                order_id = sale_orders[partner]

                partner_lines = [ol for ol in order_lines if ol.partner == partner]
                products = set(ol.product for ol in partner_lines)

                for product in sorted(products, key=lambda p: p.name):
                    product_lines = [ol for ol in partner_lines if ol.product == product]
                    qty = sum(pl.qty for pl in product_lines)
                    type = product_lines.pop().type

                    if type == 'resource':
                        self.create_order_line(
                            order_id,
                            product,
                            qty,
                        )
                    elif type == 'delivery':
                        self.create_order_line(
                            order_id,
                            product,
                            qty,
                            resource_delivery=True,
                        )
                    else:
                        self.create_order_line(
                            order_id,
                            product,
                            qty,
                            participation_line=True,
                        )

                for pl in partner_lines:
                    pl.registration.write({'sale_order_id': order_id.id})

            if activity.need_guide and activity.partner_id:
                order = sale_orders.values().pop()
                self.create_order_line(
                    order,
                    activity.guide_product_id,
                    len(activity.guides),
                    resource_guide=True,
                )

    @api.multi
    def action_quotation(self):
        for activity in self:
            for sale_order in activity.sale_orders:
                sale_order.with_context(activity_action=True).action_cancel()
                sale_order.with_context(activity_action=True).action_draft()
                activity.state = 'quotation'

    @api.multi
    def print_last_sale_order(self):
        self.ensure_one()
        sale_orders = self.sale_orders.sorted(
            lambda so: so.create_date,
            reverse=True,
        )
        if sale_orders:
            return sale_orders[0].print_quotation()
        else:
            raise ValidationError(_(
                "No Sale Order defined on this activity"
            ))

    @api.multi
    def action_sale_order(self):
        res_acti_seq = self.env.ref('resource_activity.sequence_resource_activity', False)
        for activity in self:
            vals = {'booking_type': 'booked'}
            if activity.name == '' or not activity.name:
                vals['name'] = res_acti_seq.next_by_id()

            for sale_order in activity.sale_orders:
                sale_order.with_context(activity_action=True).action_confirm()
                vals['state'] = 'sale'

            activity.write(vals)

            options = (
                activity
                .registrations
                .filtered(lambda record: record.booking_type in ['option'])
            )
            for option in options:
                option.allocations.action_confirm()
                option.write({
                    'booking_type': 'booked',
                    'state': 'booked',
                    'date_lock': None}
                )

    @api.multi
    def action_draft_to_sale(self):
        self.create_sale_order()
        self.action_sale_order()

    @api.multi
    def action_back_to_sale_order(self):
        for activity in self:
            if activity.state == 'done' and not activity.sale_orders:
                raise ValidationError(_(
                    "No sale order on this activity. Cancel first than go "
                    "back to draft. "
                ))
            activity.state = 'sale'

    def update_resource_booking_line(self, registration, sale_order_id):
        self.update_order_line(
            sale_order_id,
            True,
            {},
            registration.order_line_id,
            registration.quantity_needed,
            registration.product_id)

    def update_delivery_line(self, activity, sale_order_id, nb_delivery):

        delivery_line = (
            sale_order_id
            .order_line
            .filtered(lambda record: record.resource_delivery)
        )
        line_vals = {'resource_delivery': True}

        self.update_order_line(
            sale_order_id,
            activity.need_delivery,
            line_vals,
            delivery_line,
            nb_delivery,
            activity.delivery_product_id)

    def update_guide_line(self, activity, sale_order_id):
        guide_line = (
            activity
            .sale_order_id
            .order_line
            .filtered(lambda record: record.resource_guide == True)
        )
        line_vals = {'resource_guide': True}
        guide_qty = len(activity.guides)

        self.update_order_line(
            sale_order_id,
            activity.need_guide,
            line_vals,
            guide_line,
            guide_qty,
            activity.guide_product_id)

    def update_participation_line(self, activity, sale_order_id, nb_registrations):
        participation_line = (
            sale_order_id
            .order_line
            .filtered(lambda record: record.participation_line)
        )
        line_vals = {'participation_line': True}

        self.update_order_line(
            sale_order_id,
            activity.need_participation,
            line_vals,
            participation_line,
            nb_registrations,
            activity.participation_product_id)

    @api.multi
    def push_changes_to_sale_order(self):
        self.create_sale_order()
        for activity in self:
            activity.need_push = False
            for registration in activity.registrations:
                registration.need_push = False
        return

    def update_order_line(self,
                          order_id,
                          need_resource,
                          line_vals,
                          resource_line,
                          resource_qty,
                          resource_product_id):
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

    def has_valid_delivery(self):
        """Return True if the attribute `delivery_ids` is coherent, else
        False"""
        for activity in self:
            if activity.need_delivery:
                if len(activity.delivery_ids) != 2:
                    return False
                elif (activity.delivery_ids[0].delivery_type
                        == activity.delivery_ids[1].delivery_type):
                    return False
                elif activity.delivery_ids[0].delivery_type == '':
                    return False
                elif activity.delivery_ids[1].delivery_type == '':
                    return False
            else:
                if len(activity.delivery_ids) != 0:
                    return False
        return True

    @api.model
    def _set_valid_deliveries_cron(self):
        """Check if activities has valid deliveries. If not, valid
        deliveries are set."""
        activities = (self.env['resource.activity'].search([])
                      .filtered(
                          lambda rec: not rec.has_valid_delivery()
                      ))
        for activity in activities:
            activity.write({
                'delivery_ids': [
                    (5, False, False),
                    (0, False, {'delivery_type': 'delivery'}),
                    (0, False, {'delivery_type': 'pickup'}),
                ],
            })

    @api.model
    def create(self, vals):
        if 'need_delivery' in vals and vals.get('need_delivery'):
            vals['delivery_ids'] = [
                (0, False, {'delivery_type': 'delivery'}),
                (0, False, {'delivery_type': 'pickup'}),
            ]
        return super(ResourceActivity, self).create(vals)

    @api.multi
    def write(self, vals):
        for activity in self:
            if ('need_delivery' in vals
                    and not vals.get('need_delivery')):
                vals['delivery_ids'] = [(5,)]
            else:
                vals['delivery_ids'] = [
                    (5, False, False),
                    (0, False, {'delivery_type': 'delivery'}),
                    (0, False, {'delivery_type': 'pickup'}),
                ]

            if activity.sale_orders:
                if ('need_delivery' in vals
                        and not vals.get('need_delivery')):

                    vals['delivery_place'] = ''
                    vals['delivery_time'] = False
                    vals['pickup_place'] = ''
                    vals['pickup_time'] = False
                    vals['delivery_product_id'] = False

                if 'need_guide' in vals and not vals.get('need_guide'):
                    vals['guide_product_id'] = False
                    vals['guides'] = [[6, False, []]]

                if ('need_participation' in vals
                        and not vals.get('need_participation')):

                    vals['need_participation'] = False

                watches = (
                    'need_delivery', 'delivery_product_id',
                    'need_guide', 'guide_product_id', 'guides',
                    'need_participation', 'participation_product_id',
                    'activity_type',
                )
                if any(map(lambda var: var in vals, watches)):
                    vals['need_push'] = True
        return super(ResourceActivity, self).write(vals)

    @api.multi
    @api.depends('partner_id', 'registrations_max', 'registrations_expected')
    def _propagate_activity_fields_update(self):
        for activity in self:
            vals = {'partner_id': activity.partner_id,
                    'registrations_max': activity.registrations_max,
                    'registrations_expected': activity.registrations_expected}
            activity.registrations.write(vals)
