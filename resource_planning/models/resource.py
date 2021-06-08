# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class Resource(models.Model):
    _name = "resource.resource"
    _inherit = ["resource.resource", "mail.thread"]

    @api.model
    def _get_default_location(self):
        location = self.env.user.resource_location
        if not location:
            main_location = self.env.ref(
                "resource_planning.main_location", False
            )
            return (
                main_location
                if main_location
                else self.env["resource.location"]
            )

        return location

    category_id = fields.Many2one("resource.category", string="Category")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("available", "Available"),
            ("unavailable", "Unavailable"),
        ],
        string="State",
        default="draft",
    )
    resource_type = fields.Selection(
        [("user", "Human"), ("material", "Material")],
        string="Resource Type",
        required=True,
        default="material",
    )
    allocations = fields.One2many(
        "resource.allocation", "resource_id", string="Booking lines"
    )
    serial_number = fields.Char(string="ID number")
    location = fields.Many2one(
        "resource.location", string="Location", default=_get_default_location
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name)",
            "The name of the resource must be unique !",
        )
    ]

    @api.multi
    def action_unavailable(self):
        for resource in self:
            resource.state = "unavailable"

    @api.multi
    def action_available(self):
        for resource in self:
            resource.state = "available"

    @api.multi
    def action_draft(self):
        for resource in self:
            resource.state = "draft"

    def check_dates(self, date_start, date_end):
        if not date_start or not date_end:
            raise ValidationError(
                _("Error. Date start or date end aren't set")
            )
        elif date_end < date_start:
            raise ValidationError(
                _(
                    "Error. End date is preceding start "
                    "date. Please choose an end date after a "
                    "start date "
                )
            )

    @api.multi
    def check_availabilities(self, date_start, date_end, location):
        # todo refactor, use resource.allocation.get_allocations
        self.check_dates(date_start, date_end)
        available_resources = self.filtered(lambda r: r.state == "available")
        if location:
            available_resources = available_resources.filtered(
                lambda r: r.location.id == location.id
            )
        available_resources_ids = available_resources.ids

        # assert start < end
        conflicting_allocation_domain = [
            ("resource_id", "in", available_resources_ids),
            ("state", "!=", "cancel"),
            "!",
            "|",
            ("date_end", "<=", date_start),
            ("date_start", ">=", date_end),
        ]

        conflicting_allocations = self.env["resource.allocation"].search(
            conflicting_allocation_domain
        )
        unavailable_resources_ids = conflicting_allocations.mapped(
            "resource_id.id"
        )  # noqa

        for resource_id in unavailable_resources_ids:
            available_resources_ids.remove(resource_id)
        return available_resources_ids

    @api.multi
    def allocate_resource(
        self,
        allocation_type,
        date_start,
        date_end,
        partner_id,
        location,
        date_lock=False,
    ):
        self.check_dates(date_start, date_end)
        res_alloc = self.env["resource.allocation"]

        vals = {
            "date_start": date_start,
            "date_end": date_end,
            "date_lock": date_lock,
            "state": allocation_type,
            "partner_id": partner_id.id,
            "location": location.id,
        }

        # we check again the availabilities in case in has been booked
        # between the search and the allocation request
        allocation_ids = []
        available_resource_ids = self.check_availabilities(
            date_start, date_end, location
        )

        for resource in self.browse(available_resource_ids):
            vals["resource_id"] = resource.id
            allocation = res_alloc.create(vals)
            allocation_ids.append(allocation.id)
        return allocation_ids
