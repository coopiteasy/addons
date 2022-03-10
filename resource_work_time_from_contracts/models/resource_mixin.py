# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime
from collections import defaultdict

from pytz import timezone, utc

from odoo import fields, models
from odoo.tools import float_utils

from odoo.addons.resource.models.resource_mixin import ROUNDING_FACTOR


class ResourceMixin(models.AbstractModel):

    _inherit = "resource.mixin"

    # make this field read-only.
    resource_calendar_id = fields.Many2one("resource.calendar", readonly=True)

    def list_work_time_per_day(
        self,
        from_datetime,
        to_datetime,
        calendar=None,
        domain=None,
    ):
        if calendar or not hasattr(self, "contract_ids"):
            return super().list_work_time_per_day(
                from_datetime, to_datetime, calendar, domain
            )
        work_time_from_contracts = self._get_work_time_from_contracts(
            from_datetime, to_datetime, domain
        )
        # we need to take leaves into account. instead of going into the
        # internals of leaves themselves which are quite complex (and mostly
        # private to the resource module), we ask for the default work time
        # with and without leaves, and compute the difference, that we
        # subtract from the work time from the contracts.
        #
        # to get the default work time without leaves, we provide a domain
        # that will yield no results. the domain argument is used to query
        # leave intervals from resource.calendar.leaves (in
        # resource.resource.ResourceCalendar._leave_intervals()). the default
        # is [('time_type', '=', 'leave')]. to ensure that no leaves are
        # found, we want to use a domain that will never return anything. we
        # use [("calendar_id", "=", False)] because it will be added to
        # another domain asking for a specific calendar_id, resulting in a
        # query returning no results.
        #
        # for this, we query the calendar of the employee, which must be the
        # same as the one of the company, and which must contain full-day
        # hours for each day. this is the calendar to which leaves are linked,
        # and is used by default by
        # resource.resource_mixin.list_work_time_per_day() when calendar=None.
        default_work_time = dict(
            super().list_work_time_per_day(
                from_datetime,
                to_datetime,
                self.resource_calendar_id,
                domain=[("calendar_id", "=", False)],
            )
        )
        default_work_time_with_leaves = super().list_work_time_per_day(
            from_datetime, to_datetime, self.resource_calendar_id, domain
        )
        result = []
        for day, hours in default_work_time_with_leaves:
            total_hours = work_time_from_contracts[day] - (
                default_work_time[day] - hours
            )
            if total_hours <= 0.0:
                continue
            result.append((day, total_hours))
        return result

    def list_normal_work_time_per_day(self, from_datetime, to_datetime, domain=None):
        """
        Same as list_work_time_per_day(), but ignoring leaves
        """
        work_time_from_contracts = self._get_work_time_from_contracts(
            from_datetime, to_datetime, domain
        )
        from_datetime, to_datetime = self._localize_datetimes(
            from_datetime, to_datetime
        )
        day = from_datetime.date()
        to_day = to_datetime.date()
        delta = datetime.timedelta(days=1)
        result = []
        while day <= to_day:
            hours = work_time_from_contracts[day]
            if hours != 0.0:
                result.append((day, hours))
            day += delta
        return result

    def get_work_days_data(
        self,
        from_datetime,
        to_datetime,
        compute_leaves=True,
        calendar=None,
        domain=None,
    ):
        if calendar or not hasattr(self, "contract_ids"):
            return super().get_work_days_data(
                from_datetime, to_datetime, compute_leaves, calendar, domain
            )
        # we need the normal work time per day for each day to be able to
        # compute the fraction of day that the number of hours represents.
        # this is defined in the calendar of the employee, which must be the
        # same as the one of the company, and which must contain full-day
        # hours for each day.
        #
        # we need full days, so we replace the hours to start and stop at
        # midnight in the timezone of the resource.
        #
        # the provided domain is to exclude leaves from the computation, as
        # explained in list_work_time_per_day().
        from_datetime, to_datetime = self._localize_datetimes(
            from_datetime, to_datetime
        )
        normal_work_time_per_day = dict(
            super().list_work_time_per_day(
                from_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
                to_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
                + datetime.timedelta(days=1),
                self.resource_calendar_id,
                [("calendar_id", "=", False)],
            )
        )
        if compute_leaves:
            work_time_per_day = self.list_work_time_per_day(
                from_datetime, to_datetime, calendar=None, domain=domain
            )
        else:
            work_time_per_day = self.list_normal_work_time_per_day(
                from_datetime, to_datetime, domain=domain
            )
        num_days = 0.0
        num_hours = 0.0
        for day, work_time in work_time_per_day:
            if work_time == 0.0:
                continue
            normal_work_time = normal_work_time_per_day[day]
            # we use the same rounding computation as in
            # resource.resource_mixin.get_work_days_data().
            num_days += (
                float_utils.round(ROUNDING_FACTOR * work_time / normal_work_time)
                / ROUNDING_FACTOR
            )
            num_hours += work_time
        return {"days": num_days, "hours": num_hours}

    def _get_active_contracts(self, date_start, date_end):
        """
        Get active contracts for the provided date range.
        """
        return (
            self.env["hr.contract"]
            .sudo()
            .search(
                [
                    ("employee_id", "=", self.id),
                    ("date_start", "<=", date_end),
                    "|",
                    ("date_end", "=", None),
                    ("date_end", ">=", date_start),
                ]
            )
        )

    def _get_work_time_per_contract(
        self, contracts, from_datetime, to_datetime, domain
    ):
        """
        Return the work time per day per contract.
        """
        work_time_results = []
        for contract in contracts:
            from_dt = from_datetime
            to_dt = to_datetime
            date_start = contract.date_start
            if from_dt.date() < date_start:
                from_dt = datetime.datetime(
                    date_start.year,
                    date_start.month,
                    date_start.day,
                    tzinfo=from_dt.tzinfo,
                )
            date_end = contract.date_end
            if date_end and to_dt.date() > date_end:
                # limit to midnight on the day after date_end to completely
                # include date_end.
                to_dt = (
                    datetime.datetime(
                        date_end.year,
                        date_end.month,
                        date_end.day,
                        tzinfo=from_dt.tzinfo,
                    )
                    + datetime.timedelta(days=1)
                )
            work_time_results.append(
                super().list_work_time_per_day(
                    from_dt,
                    to_dt,
                    contract.resource_calendar_id,
                    domain,
                )
            )
        return work_time_results

    def _get_work_time_from_contracts(self, from_datetime, to_datetime, domain=None):
        from_datetime, to_datetime = self._localize_datetimes(
            from_datetime, to_datetime
        )
        contracts = self._get_active_contracts(from_datetime.date(), to_datetime.date())
        work_time_results = self._get_work_time_per_contract(
            contracts, from_datetime, to_datetime, domain
        )
        result = defaultdict(float)
        for work_time in work_time_results:
            for day, hours in work_time:
                result[day] += hours
        return result

    def _localize_datetimes(self, from_datetime, to_datetime):
        # naive datetimes are considered utc
        if not from_datetime.tzinfo:
            from_datetime = from_datetime.replace(tzinfo=utc)
        if not to_datetime.tzinfo:
            to_datetime = to_datetime.replace(tzinfo=utc)

        tz = timezone(self.tz)
        return from_datetime.astimezone(tz), to_datetime.astimezone(tz)
