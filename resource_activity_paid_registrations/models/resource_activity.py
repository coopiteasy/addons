# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResourceActivity(models.Model):
    _inherit = ["resource.activity"]

    registrations_paid = fields.Boolean(
        string="All Registrations Paid",
        compute="_compute_registrations_paid",
        store=True,
    )

    @api.multi
    @api.depends(
        "registrations.is_paid",
        "registrations.state",
        "state",
    )
    def _compute_registrations_paid(self):
        for activity in self:
            if activity.state in ("sale", "done"):
                registrations = activity.registrations.filtered(
                    lambda record: record.state == "booked"
                )

                activity.registrations_paid = all(
                    registrations.mapped("is_paid")
                )
            else:
                activity.registrations_paid = False

    @api.multi
    def mark_all_as_paid(self):
        for activity in self:
            activity.registrations.mark_as_paid()
