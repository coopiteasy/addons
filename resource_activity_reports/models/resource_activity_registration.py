# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ResourceActivityRegistration(models.Model):
    _inherit = "resource.activity.registration"

    nb_bikes = fields.Integer(
        string="Bike Registrations",
        compute="_compute_registration_statistics",
        store=True,
    )
    renting_seconds = fields.Integer(
        string="Renting Seconds",
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

    @api.multi
    @api.depends(
        "quantity",
        "quantity_allocated",
        "resource_activity_id.date_start",
        "resource_activity_id.date_end",
    )
    def _compute_registration_statistics(self):
        for registration in self:
            # if quantity allocated and no quantity (nb participants),
            # the resource allocated is not a bike
            if registration.resource_activity_id and registration.quantity > 0:
                nb_bikes = registration.quantity_allocated

                start = fields.Datetime.from_string(
                    registration.resource_activity_id.date_start
                )
                end = fields.Datetime.from_string(
                    registration.resource_activity_id.date_end
                )
                renting_seconds = nb_bikes * (end - start).seconds
                renting_hours = renting_seconds / 3600.0
                renting_days = renting_hours / 24.0

                registration.nb_bikes = nb_bikes
                registration.renting_seconds = renting_seconds
                registration.renting_hours = renting_hours
                registration.renting_days = renting_days
            else:
                registration.nb_bikes = 0
                registration.renting_seconds = 0
                registration.renting_hours = 0
                registration.renting_days = 0
