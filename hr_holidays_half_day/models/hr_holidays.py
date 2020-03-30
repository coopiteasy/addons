# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import math
from pytz import timezone, UTC

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


def floatime_to_hour_minute(f):
    decimal, integer = math.modf(f)
    return int(integer), int(round(decimal * 60))


class HrHolidays(models.Model):
    _inherit = "hr.holidays"

    period = fields.Selection(
        string="Period",
        selection=[("am", "AM"), ("pm", "PM"), ("day", "Day")],
        default="day",
    )

    @api.multi
    def onchange_date_from(self, date_to, date_from):
        res = super(HrHolidays, self).onchange_date_from(date_to, date_from)
        return self._update_values(date_to, date_from, res)

    @api.multi
    def onchange_date_to(self, date_to, date_from):
        res = super(HrHolidays, self).onchange_date_to(date_to, date_from)
        return self._update_values(date_to, date_from, res)

    def _update_values(self, date_to, date_from, res):
        employee_id = self.employee_id.id or self.env.context.get(
            "employee_id", False
        )
        if (date_to and date_from) and (date_from <= date_to):
            diff_day = self._compute_number_of_days_from_contract(
                employee_id, date_from, date_to
            )
            res["value"]["number_of_days_temp"] = diff_day
        return res

    @api.onchange("period")
    def onchange_period(self):
        if self.employee_id and self.type != "add":
            period = self.period
            from_dt = fields.Datetime.from_string(self.date_from)
            to_dt = fields.Datetime.from_string(self.date_to)

            company = self.employee_id.company_id

            if period == "am":
                from_dt, to_dt = self._replace_duration(
                    from_dt, to_dt, company.am_hour_from, company.am_hour_to
                )
            elif period == "pm":
                from_dt, to_dt = self._replace_duration(
                    from_dt, to_dt, company.pm_hour_from, company.pm_hour_to
                )
            else:
                from_dt, to_dt = self._replace_duration(
                    from_dt, to_dt, company.am_hour_from, company.pm_hour_to
                )

            self.date_from = fields.Datetime.to_string(from_dt)
            self.date_to = fields.Datetime.to_string(to_dt)

    def _replace_duration(self, date_from, date_to, hour_from, hour_to):
        hour, minute = floatime_to_hour_minute(hour_from)
        utc_date_from = self._get_utc_date(date_from, hour, minute)

        hour, minute = floatime_to_hour_minute(hour_to)
        utc_date_to = self._get_utc_date(date_to, hour, minute)

        return utc_date_from, utc_date_to

    def _get_utc_date(self, day, hour, minute):
        tz = self._context.get("tz") or self.env.user.tz
        if not tz:
            raise ValidationError(
                _("You must define a timezone for this user")
            )
        context_tz = timezone(tz)
        day_time = day.replace(hour=hour, minute=minute)
        day_local_time = context_tz.localize(day_time)
        day_utc_time = day_local_time.astimezone(UTC)
        return day_utc_time

    def _compute_number_of_days_from_contract(
        self, employee_id, date_from, date_to
    ):
        """ Returns a float equals to the timedelta between two dates given as string."""
        hours = 0.0
        if employee_id:
            employee = self.env["hr.employee"].browse(employee_id)
            company = employee.company_id
            if not company.hours_per_day:
                raise ValidationError(
                    _("You must define company working hours")
                )
            hours = (
                self.get_working_hours(employee, date_from, date_to)
                / company.hours_per_day
            )

        return hours

    @api.multi
    def get_working_hours(self, employee, date_from, date_to):
        """
        Get the working hours for a given date according to employee's contracts
        @return: total of working hours
        """
        from_dt = fields.Datetime.from_string(date_from)
        to_dt = fields.Datetime.from_string(date_to)

        total = 0.0
        contracts = self.get_contracts(employee, date_from, date_to)
        for contract in contracts:
            for calendar in contract.working_hours:
                total += sum(
                    wh
                    for wh in calendar.get_working_hours(
                        start_dt=from_dt, end_dt=to_dt,
                    )
                )
        return total

    def get_contracts(self, employee, date_from, date_to):
        """
        Get employee's contracts whose given date are included
        in the start date and the end date (defined or not) of the contract
        @return: hr.contract object
        """
        return (
            self.env["hr.contract"]
            .sudo()
            .search([("employee_id.id", "=", employee.id),])
            .filtered(
                lambda r: (
                    fields.Date.from_string(r.date_start)
                    <= fields.Date.from_string(date_from)
                )
                and (
                    not r.date_end
                    or fields.Date.from_string(date_to)
                    <= fields.Date.from_string(r.date_end)
                )
            )
        )
