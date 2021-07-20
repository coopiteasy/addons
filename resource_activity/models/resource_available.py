# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ResourceAvailable(models.Model):
    _name = "resource.available"

    name = fields.Char(related="resource_id.serial_number", string="Name")
    resource_id = fields.Many2one(
        "resource.resource", string="Resource", required=True
    )
    registration_id = fields.Many2one(
        "resource.activity.registration", string="Registration"
    )
    activity_id = fields.Many2one(
        related="registration_id.resource_activity_id",
        string="Activity",
        readonly=True,
    )
    state = fields.Selection(
        [
            ("free", "Free"),
            ("not_free", "Not free"),
            ("selected", "Selected"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        readonly=True,
    )

    @api.multi
    def action_reserve(self):
        for resource_available in self.filtered(
            lambda record: record.state == "free"
        ):
            allocation_ids = resource_available.resource_id.allocate_resource(
                resource_available.registration_id.booking_type,
                resource_available.registration_id.date_start,
                resource_available.registration_id.date_end,
                resource_available.registration_id.attendee_id,
                resource_available.registration_id.location_id,
                resource_available.registration_id.date_lock,
            )
            if allocation_ids:
                allocations = self.env["resource.allocation"].browse(
                    allocation_ids
                )
                allocations.write(
                    {
                        "activity_registration_id": resource_available.registration_id.id
                    }
                )
                resource_available.state = "selected"
                # resource_available.registration_id.quantity_allocated += 1  # mark
                resource_available.registration_id.state = (
                    resource_available.registration_id.booking_type
                )
            else:
                print "no resource found for : " + str(
                    resource_available.resource_id.ids
                )
            self.activity_id.registrations.action_refresh()
        return True

    @api.multi
    def action_cancel(self):
        allocation = self.registration_id.allocations.filtered(
            lambda record: record.resource_id.id == self.resource_id.id
            and record.state != "cancel"
        )
        allocation.action_cancel()
        self.state = "cancelled"

        return True
