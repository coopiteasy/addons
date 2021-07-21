# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from math import ceil

from openerp import api, fields, models


class ResourceActivityRegistration(models.Model):
    _inherit = "resource.activity.registration"

    nb_bikes = fields.Integer(
        string="Bike Registrations",
        compute="_compute_registration_statistics",
        store=True,
    )
    nb_accessories = fields.Integer(
        string="Accessory Registrations",
        compute="_compute_registration_statistics",
        store=True,
    )
    renting_hours = fields.Float(
        string="Renting Hours",
        compute="_compute_registration_statistics",
        # digits=(15, 3),
        store=True,
    )
    renting_days = fields.Float(
        string="Renting Days",
        compute="_compute_registration_statistics",
        # digits=(15, 3),
        store=True,
    )

    def _compute_hour_duration(self):
        self.ensure_one()
        if self.resource_activity_id:
            start = fields.Datetime.from_string(
                self.resource_activity_id.date_start
            )
            end = fields.Datetime.from_string(
                self.resource_activity_id.date_end
            )
            duration_seconds = (end - start).total_seconds()
            return duration_seconds / 3600.0
        else:
            return 0

    def _compute_day_duration(self):
        self.ensure_one()
        duration_hours = self._compute_hour_duration()

        if duration_hours == 0:
            duration_days = 0
        elif duration_hours < 4:
            duration_days = 0.5
        elif 4 <= duration_hours <= 24:
            duration_days = 1
        else:
            duration_days = ceil(duration_hours / 24.0)

        return duration_days

    @api.multi
    @api.depends(
        "quantity",
        "quantity_allocated",
        "resource_activity_id.date_start",
        "resource_activity_id.date_end",
    )
    def _compute_registration_statistics(self):
        for registration in self:
            duration_hours = registration._compute_hour_duration()
            duration_days = registration._compute_day_duration()

            # if quantity allocated and no quantity (nb participants),
            # the resource allocated is not a bike
            if registration.state == "cancelled":
                nb_bikes = 0
                nb_accessories = 0
            elif registration.quantity > 0:
                nb_bikes = registration.quantity_allocated
                nb_accessories = 0
            else:
                nb_bikes = 0
                nb_accessories = registration.quantity_allocated

            registration.nb_bikes = nb_bikes
            registration.nb_accessories = nb_accessories
            registration.renting_hours = nb_bikes * duration_hours
            registration.renting_days = nb_bikes * duration_days
