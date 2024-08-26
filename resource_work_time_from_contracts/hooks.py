# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime

from pytz import UTC, timezone

from odoo import api

from odoo.addons.hr_holidays.models.hr_leave import HolidaysRequest
from odoo.addons.resource.models.resource import float_to_time


def patch_hr_leave_onchange_request_parameters():
    if not hasattr(HolidaysRequest, "_onchange_request_parameters_original"):
        HolidaysRequest._onchange_request_parameters_original = (
            HolidaysRequest._onchange_request_parameters
        )
        # we need to remove the _onchange property of the method, otherwise it
        # will still be called.
        HolidaysRequest._onchange_request_parameters_original._onchange_original = (
            HolidaysRequest._onchange_request_parameters_original._onchange
        )
        del HolidaysRequest._onchange_request_parameters_original._onchange

    # in hr_holidays, this method reads the resource.calendar.attendance
    # records directly from the employee's or company resource.calendar to
    # find the first one and the last one corresponding to the leave date
    # range. below is a copy of the method from hr_holidays, with that part
    # replaced by a call to _get_request_attendances() to allow to change that
    # behavior.
    @api.onchange(
        "request_date_from_period",
        "request_hour_from",
        "request_hour_to",
        "request_date_from",
        "request_date_to",
        "employee_id",
    )
    def __new_onchange_request_parameters(self):
        if not self.request_date_from:
            self.date_from = False
            return

        if self.request_unit_half or self.request_unit_hours:
            self.request_date_to = self.request_date_from

        if not self.request_date_to:
            self.date_to = False
            return

        # begin change
        attendance_from, attendance_to = self._get_request_attendances()
        # end change

        if self.request_unit_half:
            if self.request_date_from_period == "am":
                hour_from = float_to_time(attendance_from.hour_from)
                hour_to = float_to_time(attendance_from.hour_to)
            else:
                hour_from = float_to_time(attendance_to.hour_from)
                hour_to = float_to_time(attendance_to.hour_to)
        elif self.request_unit_hours:
            # This hack is related to the definition of the field, basically we convert
            # the negative integer into .5 floats
            hour_from = float_to_time(
                abs(self.request_hour_from) - 0.5
                if self.request_hour_from < 0
                else self.request_hour_from
            )
            hour_to = float_to_time(
                abs(self.request_hour_to) - 0.5
                if self.request_hour_to < 0
                else self.request_hour_to
            )
        elif self.request_unit_custom:
            hour_from = self.date_from.time()
            hour_to = self.date_to.time()
        else:
            hour_from = float_to_time(attendance_from.hour_from)
            hour_to = float_to_time(attendance_to.hour_to)
        self.date_from = (
            timezone(self.tz)
            .localize(datetime.combine(self.request_date_from, hour_from))
            .astimezone(UTC)
            .replace(tzinfo=None)
        )
        self.date_to = (
            timezone(self.tz)
            .localize(datetime.combine(self.request_date_to, hour_to))
            .astimezone(UTC)
            .replace(tzinfo=None)
        )
        self._onchange_leave_dates()

    HolidaysRequest._onchange_request_parameters = __new_onchange_request_parameters


def post_load_hook():
    patch_hr_leave_onchange_request_parameters()
