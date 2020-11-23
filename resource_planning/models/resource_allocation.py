# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ResourceAllocation(models.Model):
    _name = "resource.allocation"

    # _inherit = ['mail.thread']

    name = fields.Many2one(related="partner_id")
    serial_number = fields.Char(
        related="resource_id.serial_number", string="Serial number"
    )
    resource_id = fields.Many2one(
        "resource.resource", string="Resource", required=True
    )
    resource_category_id = fields.Many2one(
        related="resource_id.category_id",
        string="Resource Category",
        store=True,
    )
    date_start = fields.Datetime(string="Date start")
    date_end = fields.Datetime(string="Date end")
    state = fields.Selection(
        [
            ("booked", "Booked"),
            ("option", "Option"),
            ("maintenance", "Maintenance"),
            ("cancel", "Cancel"),
        ],
        string="State",
        default="option",
    )
    date_lock = fields.Date(
        string="Lock date",
        help="If the booking type is option, it should be confirmed before "
        "the lock date expire",
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    location = fields.Many2one("resource.location", string="Location")

    @api.multi
    def action_confirm(self):
        for allocation in self:
            allocation.write({"state": "booked", "date_lock": None})

    @api.multi
    def action_cancel(self):
        for allocation in self:
            allocation.state = "cancel"

    @api.multi
    def action_option(self):
        for allocation in self:
            allocation.state = "option"
