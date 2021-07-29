# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from collections import namedtuple
from datetime import datetime, timedelta

import pytz

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

OrderLine = namedtuple(
    "OrderLine", ["partner", "product", "qty", "type", "registration"]
)


# fixme use Datetime.from_string
def _pd(dt):
    """parse datetime"""
    return datetime.strptime(dt, DTF) if dt else dt


class ResourceActivity(models.Model):
    _name = "resource.activity"
    _inherit = ["mail.thread"]
    _order = "date_start"

    @api.multi
    @api.depends("registrations.need_push")
    def _compute_push2sale_order(self):
        # computed field in order to display or not the push to sale order
        # button
        for activity in self:
            if activity.sale_orders:
                registrations_need_push = any(
                    activity.registrations.mapped("need_push")
                )
                activity.need_push = (
                    activity.need_push or registrations_need_push
                )
        return

    @api.multi
    def _compute_booked_resources(self):
        for activity in self:
            booked_resources = []
            for registration in activity.registrations:
                res_ids = (
                    registration.allocations.filtered(
                        lambda record: record.state in ["option", "booked"]
                    )
                    .mapped("resource_id")
                    .ids
                )
                if res_ids:
                    booked_resources = booked_resources + res_ids
            activity.booked_resources = booked_resources

    @api.multi
    def _compute_sale_orders(self):
        for activity in self:
            activity.sale_orders = (
                self.env["sale.order"]
                .search([("activity_id", "=", activity.id)])
                .ids
            )

    @api.multi
    @api.depends("date_start")
    def _compute_dayofweek(self):
        """
        The date convertion in python depend on the LC_ALL variable.
        To get a deterministic behaviour, number of the day is used.
        0 to Sunday to 6 for Saturday.
        """
        for activity in self:
            activity.dayofweek = datetime.strftime(
                fields.Date.from_string(activity.date_start), "%w"
            )

    def _default_location(self):
        location = self.env.user.resource_location
        if location:
            return location
        else:
            raise UserError(_("No location set for current user"))

    name = fields.Char(string="Name", copy=False)
    partner_id = fields.Many2one(
        "res.partner", string="Customer", domain=[("customer", "=", True)]
    )
    participation_product_id = fields.Many2one(
        "product.product",
        string="Product Participation",
        domain=[("is_participation", "=", True)],
    )
    dayofweek = fields.Selection(
        selection=[
            ("1", "Monday"),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
            ("6", "Saturday"),
            ("0", "Sunday"),
        ],
        string="Day",
        compute="_compute_dayofweek",
    )
    date_start = fields.Datetime(string="Date start", required=True)
    date_end = fields.Datetime(string="Date end", required=True)
    duration = fields.Char(
        string="Duration", compute="_compute_duration", store=True
    )
    registrations = fields.One2many(
        "resource.activity.registration",
        "resource_activity_id",
        string="Registration",
    )
    location_id = fields.Many2one(
        "resource.location",
        string="Location",
        required=True,
        default=_default_location,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("quotation", "Quotation"),
            ("sale", "Sale"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="draft",
    )
    date_lock = fields.Date(string="Date lock")
    booking_type = fields.Selection(
        [("option", "Option"), ("booked", "Booking")],
        string="Booking type",
        required=True,
        default="booked",
    )
    active = fields.Boolean("Active", default=True)
    departure = fields.Char(string="Departure")
    arrival = fields.Char(string="Arrival")
    description = fields.Char(string="Description")
    internal_comment = fields.Html(string="Internal Comment")
    activity_type = fields.Many2one(
        "resource.activity.type", string="Activity type", required=True
    )
    analytic_account = fields.Many2one(
        related="activity_type.analytic_account",
        string="Analytic account",
        readonly=True,
        groups="analytic.group_analytic_accounting",
    )
    trainers = fields.Many2many(
        "res.partner",
        relation="activity_trainer",
        column1="activity_id",
        column2="trainer_id",
        string="Trainer",
        domain=[("is_trainer", "=", True)],
    )
    langs = fields.Many2many("resource.activity.lang", string="Langs")
    activity_theme = fields.Many2one(
        "resource.activity.theme", string="Activity theme"
    )
    need_participation = fields.Boolean(string="Need participation?")
    set_allocation_span = fields.Boolean(
        string="Set Allocation Span Manually", default=False
    )
    resource_allocation_start = fields.Datetime(
        string="Resource Allocation Start"
    )
    resource_allocation_end = fields.Datetime(string="Resource Allocation End")
    registrations_max = fields.Integer(string="Maximum registration")
    registrations_min = fields.Integer(string="Minimum registration")
    registrations_expected = fields.Integer(
        string="Registrations made",
        store=True,
        readonly=True,
        compute="_compute_registrations",
    )
    nb_allocated_resources = fields.Integer(
        string="Allocated Resources",
        compute="_compute_registrations",
    )
    without_resource_reg = fields.Integer(
        string="Registrations without resource",
        store=True,
        readonly=True,
        compute="_compute_registrations",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        change_default=True,
        readonly=True,
        default=lambda self: self.env["res.company"]._company_default_get(),
    )
    need_push = fields.Boolean(
        string="Need to push to sale order",
        compute="_compute_push2sale_order",
        store=True,
    )
    booked_resources = fields.One2many(
        "resource.resource",
        string="Booked resources",
        compute="_compute_booked_resources",
    )
    sale_orders = fields.One2many(
        "sale.order", string="Sale orders", compute="_compute_sale_orders"
    )

    available_category_ids = fields.One2many(
        comodel_name="resource.category.available",
        inverse_name="activity_id",
        string="Available Bikes Per Category",
        compute="_compute_available_categories",
        store=True,
    )

    @api.multi
    @api.depends(
        "date_start", "date_end", "location_id", "registrations.state"
    )
    def _compute_available_categories(self):
        for activity in self:
            activity.available_category_ids = [(5, 0, 0)]  # reset field
            if (
                activity.date_start
                and activity.date_end
                and activity.location_id
            ):
                available_categories = self.env[
                    "resource.category"
                ].get_available_categories(
                    date_start=activity.date_start,
                    date_end=activity.date_end,
                    location=activity.location_id,
                )
                update_values = [
                    (
                        0,
                        0,
                        {
                            "activity_id": activity.id,
                            "category_id": category_id,
                            "nb_resources": nb_resources,
                        },
                    )
                    for category_id, nb_resources in available_categories.items()
                ]
                activity.available_category_ids = update_values

    @api.onchange("location_id")
    def onchange_location_id(self):
        if self.location_id and self.location_id.address:
            self.departure = self.location_id.address._display_address(
                self.location_id.address
            )
            self.arrival = self.location_id.address._display_address(
                self.location_id.address
            )

    @api.onchange("booking_type")
    def onchange_booking_type(self):
        if self.booking_type == "booked":
            self.date_lock = None

    def _localize(self, date):
        tz = (
            pytz.timezone(self._context["tz"])
            if self._context["tz"]
            else pytz.utc
        )
        return pytz.utc.localize(date).astimezone(tz)

    def _trunc_day(self, datetime_):
        datetime_ = self._localize(_pd(datetime_))
        datetime_ = datetime_.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return datetime_.astimezone(pytz.utc)

    @api.onchange(
        "date_start",
        "set_allocation_span",
    )
    def _onchange_allocation_start(self):
        """
        Sets allocation start date_start
        resource_allocation_start can however still be
        manually set by user if set_allocation_span is true.
        """
        if self.date_start:
            self.resource_allocation_start = self.date_start

    @api.onchange(
        "date_end",
        "set_allocation_span",
    )
    def _onchange_allocation_end(self):
        """
        sets allocation end to date_end.
        resource_allocation_end can however still be
        manually set by user if set_allocation_span is true.
        """
        if self.date_end:
            self.resource_allocation_end = self.date_end

    @api.one
    @api.constrains("date_start", "date_end")
    def _check_date(self):
        if self.date_end < self.date_start:
            raise ValidationError(_("Date end can't be before date start:"))

    @api.one
    @api.constrains(
        "date_start",
        "date_end",
        "resource_allocation_start",
        "resource_allocation_end",
    )
    def _check_booked_resources_blocks_dates(self):
        if self.booked_resources:
            raise ValidationError(
                _(
                    "You cannot modify activity dates, resource allocation dates "
                    "when a resource is already booked. "
                    "You must either delete this activity and create a new one or "
                    "release all booked resources for this activity."
                )
            )

    @api.multi
    @api.depends(
        "registrations_max", "registrations.state", "registrations.quantity"
    )
    def _compute_registrations(self):
        for activity in self:
            registrations = activity.registrations.filtered(
                lambda record: record.state != "cancelled"
            )

            activity.registrations_expected = sum(
                registrations.mapped("quantity")
            )
            activity.without_resource_reg = sum(
                map(
                    lambda reg: reg.quantity - reg.quantity_needed,
                    registrations,
                )
            )
            activity.nb_allocated_resources = sum(
                registrations.mapped("quantity_allocated")
            )

    @api.multi
    @api.depends("date_end", "date_start")
    def _compute_duration(self):
        period = timedelta(days=1)
        period_time = timedelta(hours=24)

        for activity in self:
            if (
                activity.date_start
                and activity.date_end
                and activity.date_start < activity.date_end
            ):

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
        registrations = self.env["resource.activity.registration"].browse()
        for activity in self:
            for registration in activity.registrations:
                if registration.state == "booked":
                    registrations |= registration
        registrations.action_cancel()
        registrations.action_draft()

    @api.multi
    def action_done(self):
        """
        Allowed from
        - sale state
        - draft state if nothing to invoice
        - allow but warn from draft state with invoiced resources
        """
        for activity in self:
            if activity.state == "sale":
                activity.state = "done"
            else:
                raise ValidationError(
                    _("You can only set the activity to done from Sale state.")
                )

    @api.multi
    def action_draft(self):
        for activity in self:
            activity.state = "draft"

    @api.multi
    def action_cancel(self):
        action = self.env.ref("resource_activity.action_cancel_sale_order")
        for activity in self:
            activity.registrations.action_cancel()
            activity.state = "cancelled"

            return {
                "name": action.name,
                "help": action.help,
                "type": action.type,
                "view_type": action.view_type,
                "view_mode": action.view_mode,
                "target": action.target,
                "context": self._context,
                "res_model": action.res_model,
            }

    # move to sale order line ?
    def _create_order_line(self, order, line_type, product, qty):
        line_values = {
            "order_id": order.id,
            "product_id": product.id,
            "product_uom_qty": qty,
            "product_uom": product.uom_id.id,
        }

        if line_type == "participation":
            line_values.update(participation_line=True)

        order_line = self.env["sale.order.line"].create(line_values)
        order_line.update_line()
        return order_line

    def _prepare_lines(self):
        """Returns a list of OrderLine based on activity registrations"""
        self.ensure_one()
        registrations = self.registrations.filtered(
            lambda record: record.state != "cancelled"
        )
        prepared_lines = []
        for registration in registrations:
            if self.partner_id:
                partner = self.partner_id.id
            else:
                partner = registration.attendee_id.id

            if self.need_participation:
                prepared_lines.append(
                    OrderLine(
                        partner,
                        self.participation_product_id,
                        registration.quantity,
                        "participation",
                        registration,
                    )
                )
            if registration.quantity_needed > 0:
                prepared_lines.append(
                    OrderLine(
                        partner,
                        registration.product_id,
                        registration.quantity_needed,
                        "resource",
                        registration,
                    )
                )

        return prepared_lines

    def _create_sale_order(self, activity, partner_id):
        order = self.env["sale.order"].create(
            {
                "partner_id": partner_id,
                "activity_id": activity.id,
                "project_id": activity.analytic_account.id,
                "activity_sale": True,
            }
        )
        activity.state = "quotation"
        return order

    def _prepare_sale_orders(self, activity):
        """
        create empty sale order for each partner
         or get sale order ids and unlink sale order lines
        :param activity:
        :return:
        """
        registrations = activity.registrations.filtered(
            lambda record: record.state != "cancelled"
        )

        # could probably be a whole lot simpler
        sale_orders = {}
        for registration in registrations:
            if activity.partner_id:
                partner = activity.partner_id.id
            else:
                partner = registration.attendee_id.id

            if partner not in sale_orders:
                if (
                    registration.sale_order_id
                    and registration.sale_order_id.state != "cancel"
                ):
                    sale_orders[partner] = registration.sale_order_id
                    for order_line in registration.sale_order_id.order_line:
                        order_line.unlink()
                else:
                    order_id = self._create_sale_order(activity, partner)
                    sale_orders[partner] = order_id

        # cringe, refactor when unit tested
        if not registrations and activity.partner_id:
            partner = activity.partner_id.id
            order_id = self._create_sale_order(activity, partner)
            sale_orders[partner] = order_id

        return sale_orders

    @api.multi
    def create_sale_order(self):
        for activity in self:

            order_lines = self._prepare_lines()
            if not order_lines:
                raise ValidationError(
                    _("Nothing to invoice on this activity.")
                )

            sale_orders = self._prepare_sale_orders(activity)

            partners = set(ol.partner for ol in order_lines)
            for partner in partners:
                order_id = sale_orders[partner]

                partner_lines = [
                    ol for ol in order_lines if ol.partner == partner
                ]
                products = set(ol.product for ol in partner_lines)

                for product in sorted(products, key=lambda p: p.name):
                    product_lines = [
                        ol for ol in partner_lines if ol.product == product
                    ]
                    qty = sum(pl.qty for pl in product_lines)
                    type = product_lines.pop().type

                    self._create_order_line(
                        order_id,
                        type,
                        product,
                        qty,
                    )

            for pl in partner_lines:
                if pl.registration:
                    pl.registration.write({"sale_order_id": order_id.id})

    @api.multi
    def action_quotation(self):
        for activity in self:
            for sale_order in activity.sale_orders:
                sale_order.with_context(activity_action=True).action_cancel()
                sale_order.with_context(activity_action=True).action_draft()
                activity.state = "quotation"

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
            raise ValidationError(_("No Sale Order defined on this activity"))

    @api.multi
    def action_sale_order(self):
        res_acti_seq = self.env.ref(
            "resource_activity.sequence_resource_activity", False
        )
        for activity in self:
            vals = {"booking_type": "booked"}
            if activity.name == "" or not activity.name:
                vals["name"] = res_acti_seq.next_by_id()

            for sale_order in activity.sale_orders:
                sale_order.with_context(activity_action=True).action_confirm()
                vals["state"] = "sale"

            activity.write(vals)

            options = activity.registrations.filtered(
                lambda record: record.booking_type in ["option"]
            )
            for option in options:
                option.allocations.action_confirm()
                option.write(
                    {
                        "booking_type": "booked",
                        "state": "booked",
                        "date_lock": None,
                    }
                )

    @api.multi
    def action_draft_to_sale(self):
        self.create_sale_order()
        self.action_sale_order()

    @api.multi
    def action_back_to_sale_order(self):
        for activity in self:
            if activity.state == "done" and not activity.sale_orders:
                raise ValidationError(
                    _(
                        "No sale order on this activity. Cancel first than go "
                        "back to draft. "
                    )
                )
            activity.state = "sale"

    def update_resource_booking_line(self, registration, sale_order_id):
        self.update_order_line(
            sale_order_id,
            True,
            {},
            registration.order_line_id,
            registration.quantity_needed,
            registration.product_id,
        )

    def update_participation_line(
        self, activity, sale_order_id, nb_registrations
    ):
        participation_line = sale_order_id.order_line.filtered(
            lambda record: record.participation_line
        )
        line_vals = {"participation_line": True}

        self.update_order_line(
            sale_order_id,
            activity.need_participation,
            line_vals,
            participation_line,
            nb_registrations,
            activity.participation_product_id,
        )

    @api.multi
    def push_changes_to_sale_order(self):
        self.create_sale_order()
        for activity in self:
            activity.need_push = False
            for registration in activity.registrations:
                registration.need_push = False
        return

    def update_order_line(
        self,
        order_id,
        need_resource,
        line_vals,
        resource_line,
        resource_qty,
        resource_product_id,
    ):
        if need_resource:
            line_vals["product_uom_qty"] = resource_qty
            line_vals["product_id"] = resource_product_id.id
            if resource_line:
                resource_line.write(line_vals)
                resource_line.update_line()
            else:
                line_vals["order_id"] = order_id.id
                line_vals["product_uom"] = resource_product_id.uom_id.id
                self.env["sale.order.line"].create(line_vals)
        else:
            if resource_line:
                resource_line.unlink()

    @api.multi
    def write(self, vals):
        for activity in self:
            if activity.sale_orders:
                if "need_participation" in vals and not vals.get(
                    "need_participation"
                ):
                    # reset participation fields
                    # I (Robin) think this should be removed
                    vals["need_participation"] = False

                # if sale order was generated and these values
                #   are updated, the sale order is flagged as
                #   "need push to sale order"
                watches = (
                    "need_participation",
                    "participation_product_id",
                    "activity_type",
                )
                if any(map(lambda var: var in vals, watches)):
                    vals["need_push"] = True
        return super(ResourceActivity, self).write(vals)

    @api.multi
    @api.depends("partner_id", "registrations_max", "registrations_expected")
    def _propagate_activity_fields_update(self):
        for activity in self:
            vals = {
                "partner_id": activity.partner_id,
                "registrations_max": activity.registrations_max,
                "registrations_expected": activity.registrations_expected,
            }
            activity.registrations.write(vals)
