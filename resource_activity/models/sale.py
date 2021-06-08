# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class ResCompany(models.Model):
    _inherit = "res.company"
    sale_note_html_id = fields.Many2one(
        comodel_name="res.company.note",
        string="Default Terms and Conditions",
    )


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _default_note_html(self):
        return self.env.user.company_id.sale_note_html_id

    activity_sale = fields.Boolean(string="Activity Sale?")
    activity_id = fields.Many2one(
        "resource.activity", string="Activity", readonly=True
    )
    location_id = fields.Many2one(
        related="activity_id.location_id", string="Location", readonly=True
    )
    departure = fields.Char(
        related="activity_id.departure", string="Departure", readonly=True
    )
    arrival = fields.Char(
        related="activity_id.arrival", string="Arrival", readonly=True
    )
    date_start = fields.Datetime(
        related="activity_id.date_start", string="Date start", readonly=True
    )
    date_end = fields.Datetime(
        related="activity_id.date_end", string="Date end", readonly=True
    )
    duration = fields.Char(
        related="activity_id.duration", string="Duration", readonly=True
    )
    langs = fields.Many2many(
        related="activity_id.langs", string="Langs", readonly=True
    )
    registrations_expected = fields.Integer(
        related="activity_id.registrations_expected",
        string="Expected registrations",
        readonly=True,
    )
    activity_type = fields.Many2one(
        related="activity_id.activity_type",
        string="Activity type",
        readonly=True,
    )
    activity_theme = fields.Many2one(
        related="activity_id.activity_theme",
        string="Activity theme",
        readonly=True,
    )
    need_delivery = fields.Boolean(
        related="activity_id.need_delivery",
        string="Need delivery?",
        readonly=True,
    )
    delivery_place = fields.Char(
        related="activity_id.delivery_place",
        string="Delivery place",
        readonly=True,
    )
    delivery_time = fields.Datetime(
        related="activity_id.delivery_time",
        string="Delivery time",
        readonly=True,
    )
    pickup_place = fields.Char(
        related="activity_id.pickup_place",
        string="Pick up place",
        readonly=True,
    )
    pickup_time = fields.Datetime(
        related="activity_id.pickup_time", string="Pick up time", readonly=True
    )
    description = fields.Char(
        related="activity_id.description", string="Description", readonly=True
    )
    booked_resources = fields.One2many(
        "resource.resource",
        related="activity_id.booked_resources",
        readonly=True,
    )
    note_html_id = fields.Many2one(
        comodel_name="res.company.note",
        string="Terms and conditions",
    )

    @api.model
    def create(self, vals):
        sale_order = super(SaleOrder, self).create(vals)
        sale_order._set_note_html_id()
        return sale_order

    @api.model
    def _set_note_html_id(self):
        self.ensure_one()
        if self.activity_id:
            activity = self.activity_id
            sale_note_html_id = (
                activity.location_id.terms_ids.filtered(
                    lambda r: r.note_id.active
                          and r.location_id == activity.location_id
                          and r.activity_type_id == activity.activity_type
                ).note_id
                or self._default_note_html()
            )
            self.note_html_id = sale_note_html_id

    @api.multi
    def action_draft(self):
        if self.activity_sale and not self.env.context.get("activity_action"):
            raise UserError(
                _(
                    "You can't set to draft a sale order linked to "
                    "an activity. Please go to the activity to "
                    "perform this operation"
                )
            )
        return super(SaleOrder, self).action_draft()

    @api.multi
    def action_cancel(self):
        if self.activity_sale and not self.env.context.get("activity_action"):
            raise UserError(
                _(
                    "You can't cancel a sale order linked to an "
                    "activity. Please go to the activity to perform"
                    " this operation"
                )
            )
        return super(SaleOrder, self).action_cancel()

    @api.multi
    def action_confirm(self):
        if self.activity_sale and not self.env.context.get("activity_action"):
            raise UserError(
                _(
                    "You can't confirm a sale order linked to an "
                    "activity. Please go to the activity to perform"
                    " this operation"
                )
            )
        return super(SaleOrder, self).action_confirm()

    @api.multi
    def action_open_sale_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sale Order",
            "view_type": "form",
            "view_mode": "form",
            "res_model": self._name,
            "res_id": self.id,
            "target": "current",
        }

    @api.multi
    def get_category_quantity(self):
        category_qty = {}
        for booked_resource in self.booked_resources:
            category_qty[booked_resource.category_id.name] = (
                category_qty.get(booked_resource.category_id.name, 0) + 1
            )
        return category_qty

    @api.model
    def cron_init_note_html(self):
        for sale_order in self.search([]):
            sale_order._set_note_html_id()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    resource_delivery = fields.Boolean(string="Resource Delivery")
    resource_guide = fields.Boolean(string="Resource Guide")
    participation_line = fields.Boolean(string="Participation")

    @api.multi
    def update_line(self):
        onchange_fields = ["name", "price_unit", "product_uom", "tax_id"]
        for line in self:
            line.product_id_change()

            values = {}
            for field in onchange_fields:
                if field not in values:
                    values[field] = line._fields[field].convert_to_write(
                        line[field]
                    )
            line.write(values)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_delivery = fields.Boolean(string="Delivery")
    is_guide = fields.Boolean(string="Guide")
    is_participation = fields.Boolean(string="Participation")
