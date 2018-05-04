# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from datetime import date
from openerp.exceptions import ValidationError, UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    activity_sale = fields.Boolean(string="Activity Sale?")
    activity_id = fields.Many2one('resource.activity', string="Activity", readonly=True)
    location_id = fields.Many2one(related="activity_id.location_id",string="Location", readonly=True)
    departure = fields.Char(related="activity_id.departure", string="Departure", readonly=True)
    arrival = fields.Char(related="activity_id.arrival", string="Arrival", readonly=True)
    date_start = fields.Datetime(related="activity_id.date_start", string="Date start", readonly=True)
    date_end = fields.Datetime(related="activity_id.date_end", string="Date end", readonly=True)
    duration = fields.Char(related="activity_id.duration", string="Duration", readonly=True)
    langs = fields.Many2many(related="activity_id.langs", string="Langs", readonly=True)
    registrations_expected = fields.Integer(related="activity_id.registrations_expected", string="Expected registrations", readonly=True)
    activity_type = fields.Many2one(related="activity_id.activity_type", string="Activity type", readonly=True)
    activity_theme = fields.Many2one(related="activity_id.activity_theme", string="Activity theme", readonly=True)
    need_delivery = fields.Boolean(related="activity_id.need_delivery", string="Need delivery?", readonly=True)
    delivery_place = fields.Char(related="activity_id.delivery_place", string="Delivery place", readonly=True)
    delivery_time = fields.Char(related="activity_id.delivery_time", string="Delivery time", readonly=True)
    