# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ResourceActivity(models.Model):
    _inherit = "resource.activity"

    registration_state = fields.Selection(
        string="Registration State",
        selection=[("booked", "Booked"), ("waiting", "Waiting")],
        compute="_compute_registration_state",
        store=True,
        help="Booked if all registrations are booked, waiting otherwise",
    )

    @api.multi
    @api.depends("registrations.state")
    def _compute_registration_state(self):
        for activity in self:
            registrations = activity.registrations.filtered(
                lambda r: r.state not in ("draft", "cancelled")
            )
            is_booked = all(r.state == "booked" for r in registrations)
            activity.registration_state = "booked" if is_booked else "waiting"
