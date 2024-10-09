# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime
import math
import warnings
from collections import defaultdict

from pytz import timezone, utc

from odoo import models
from odoo.tools import float_utils

from odoo.addons.resource.models.resource import Intervals
from odoo.addons.resource.models.resource_mixin import ROUNDING_FACTOR

DAY_ROUNDING_MODE_PARAM = "resource_work_time_from_contracts.day_rounding_mode"
DAY_ROUNDING_GRANULARITY_PARAM = (
    "resource_work_time_from_contracts.day_rounding_granularity"
)
DAY_ROUNDING_MODE_NONE = "none"
DAY_ROUNDING_MODE_ROUND = "round"
DAY_ROUNDING_MODE_CEIL = "ceil"
DAY_ROUNDING_CEIL_THRESHOLD = 0.01
DEFAULT_DAY_ROUNDING_GRANULARITY = 1


class ResourceMixin(models.AbstractModel):
    _inherit = "resource.mixin"

    def get_work_days_data(
        self,
        from_datetime,
        to_datetime,
        compute_leaves=True,
        calendar=None,
        domain=None,
    ):
        # sudo() is needed for normal users that have no read access to
        # contracts because hasattr() tries to access the field's value.
        if calendar or not hasattr(self.sudo(), "contract_ids"):
            return super().get_work_days_data(
                from_datetime, to_datetime, compute_leaves, calendar, domain
            )
        # we need the expected attendance time per day for each day to be able
        # to compute the fraction of day that the number of hours represents.
        # we choose to use the resource.calendar.hours_per_day field for this.
        # it is automatically computed, but can be edited. this way, it is
        # possible to have irregular work schedules, for example where some
        # days only have a half day, and taking a leave on these will be
        # counted as a half day instead of as a full day.
        #
        # we need full days, so we replace the hours to start and stop at
        # midnight in the timezone of the resource.
        from_datetime, to_datetime = self._localize_datetimes(
            from_datetime, to_datetime
        )
        attendance_intervals = self._get_attendance_intervals(
            from_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
            to_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            + datetime.timedelta(days=1),
        )
        attendance_time_per_day = dict(
            self._expected_attendance_per_day_from_intervals(attendance_intervals)
        )
        if compute_leaves:
            work_time_per_day = self.list_work_time_per_day(
                from_datetime, to_datetime, calendar=None, domain=domain
            )
        else:
            work_time_per_day = self.list_attendance_time_per_day(
                from_datetime, to_datetime
            )
        return self._sum_work_days_data(work_time_per_day, attendance_time_per_day)

    def list_work_time_per_day(
        self,
        from_datetime,
        to_datetime,
        calendar=None,
        domain=None,
    ):
        # sudo() is needed for normal users that have no read access to
        # contracts because hasattr() tries to access the field's value.
        if calendar or not hasattr(self.sudo(), "contract_ids"):
            return super().list_work_time_per_day(
                from_datetime, to_datetime, calendar, domain
            )
        work_intervals = self._get_work_intervals(from_datetime, to_datetime, domain)
        return self._sum_hours_per_date_from_intervals(work_intervals)

    def list_attendance_time_per_day(self, from_datetime, to_datetime):
        """
        Same as list_work_time_per_day(), but ignoring leaves
        """
        intervals = self._get_attendance_intervals(from_datetime, to_datetime)
        return self._sum_hours_per_date_from_intervals(intervals)

    def list_normal_work_time_per_day(self, from_datetime, to_datetime):
        warnings.warn(
            "resource.mixin.list_normal_work_time_per_day() is deprecated. "
            "please use .list_attendance_time_per_day() instead.",
            DeprecationWarning,
        )
        return self.list_attendance_time_per_day(from_datetime, to_datetime)

    def get_attendances_of_date_range(self, date_from, date_to):
        """
        Get the first and last resource.calendar.attendance corresponding to
        the range defined by date_from and date_to.
        """
        contracts = self._get_active_contracts(date_from, date_to)
        if not contracts:
            (
                first_attendance,
                last_attendance,
            ) = self.resource_calendar_id.get_first_last_attendance(date_from, date_to)
            if first_attendance is None:
                return (None, None)
            return (first_attendance[1], last_attendance[1])
        earliest_attendance = None
        latest_attendance = None
        for contract in contracts:
            (
                attendance_from,
                attendance_to,
            ) = contract.resource_calendar_id.get_first_last_attendance(
                max(date_from, contract.date_start),
                min(date_to, contract.date_end or date_to),
            )
            if attendance_from is not None and (
                earliest_attendance is None
                or attendance_from[0] < earliest_attendance[0]
                or (
                    attendance_from[0] == earliest_attendance[0]
                    and attendance_from[1].hour_from < earliest_attendance[1].hour_from
                )
            ):
                earliest_attendance = attendance_from
            if attendance_to is not None and (
                latest_attendance is None
                or attendance_to[0] > latest_attendance[0]
                or (
                    attendance_to[0] == latest_attendance[0]
                    and attendance_to[1].hour_to > latest_attendance[1].hour_to
                )
            ):
                latest_attendance = attendance_to
        if earliest_attendance is None:
            return (None, None)
        return (earliest_attendance[1], latest_attendance[1])

    def get_calendar_for_date(self, date):
        """
        Get the resource.calendar of the contract that applies to the provided
        date.
        """
        # there can be multiple contracts active at the same time. only the
        # first one found will be used.
        current_contracts = self._get_active_contracts(date, date)
        if not current_contracts:
            return None
        return current_contracts[0].resource_calendar_id

    def _expected_attendance_per_day_from_intervals(self, intervals):
        """
        Get the number of expected attendance hours per day from a list of
        intervals.
        """
        # instead of computing the real number of hours per day from the
        # intervals, we take the value of hours_per_day from their calendar.
        # this allows to configure the duration of a day for each calendar,
        # which allows for half days to be computed as half days instead of
        # full days.
        #
        # for each day, we compute the average of the hours_per_day
        # of the calendar of all intervals of that day (independently of their
        # length). if they come from the same calendar, it will result in the
        # same value, but in case of overlapping calendars with different
        # values, it will compute the average value.
        hours_per_day = defaultdict(list)
        for start, stop, attendances in intervals:
            # matching intervals can have multiple attendances.
            for attendance in attendances:
                hours_per_day[start.date()].append(attendance.calendar_id.hours_per_day)
        result = []
        for date, hours in hours_per_day.items():
            result.append((date, sum(hours) / len(hours)))
        return sorted(result)

    def _get_round_day_func(self, rounding_mode, granularity):
        """
        Get the day rounding function according to the provided rounding_mode
        and granularity.
        """

        def round_day_default(work_time, attendance_time):
            # this is the same rounding computation as in
            # resource.resource_mixin.get_work_days_data().
            return (
                float_utils.round(ROUNDING_FACTOR * work_time / attendance_time)
                / ROUNDING_FACTOR
            )

        def round_day_round(work_time, attendance_time):
            return (
                float_utils.round((work_time / attendance_time) / granularity)
                * granularity
            )

        def round_day_ceil(work_time, attendance_time):
            return (
                math.ceil(
                    (work_time / attendance_time) / granularity
                    - granularity * DAY_ROUNDING_CEIL_THRESHOLD
                )
                * granularity
            )

        if rounding_mode == DAY_ROUNDING_MODE_ROUND:
            return round_day_round
        if rounding_mode == DAY_ROUNDING_MODE_CEIL:
            return round_day_ceil
        return round_day_default

    def _get_day_rounding_func(self):
        """
        Get the day rounding function from the system parameters.
        """
        ir_config_parameter_model = self.env["ir.config_parameter"].sudo()
        rounding_mode = ir_config_parameter_model.get_param(DAY_ROUNDING_MODE_PARAM)
        rounding_granularity = ir_config_parameter_model.get_param(
            DAY_ROUNDING_GRANULARITY_PARAM
        )
        if rounding_granularity:
            rounding_granularity = float(rounding_granularity)
        else:
            rounding_granularity = DEFAULT_DAY_ROUNDING_GRANULARITY
        return self._get_round_day_func(rounding_mode, rounding_granularity)

    def _sum_work_days_data(self, work_time_per_day, attendance_time_per_day):
        num_days = 0.0
        num_hours = 0.0
        round_day = self._get_day_rounding_func()
        for day, work_time in work_time_per_day:
            if work_time == 0.0:
                continue
            attendance_time = attendance_time_per_day[day]
            num_days += round_day(work_time, attendance_time)
            num_hours += work_time
        return {"days": num_days, "hours": num_hours}

    def _sum_hours_per_date_from_intervals(self, intervals):
        """
        Sum the provided intervals as number of hours per date.

        Return a list of tuples of the form (date, hours).
        """
        result = defaultdict(float)
        for start, stop, meta in intervals:
            result[start.date()] += (stop - start).total_seconds() / 3600
        return sorted(result.items())

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

    def _get_attendance_intervals_of_calendar(
        self, calendar, from_datetime, to_datetime
    ):
        """
        Return the attendance intervals for the provided resource.calendar,
        ignoring leaves.
        """
        return calendar._attendance_intervals(
            from_datetime, to_datetime, self.resource_id
        )

    def _get_attendance_intervals_of_contracts(
        self, contracts, from_datetime, to_datetime
    ):
        """
        Return the attendance intervals for from_datetime to to_datetime
        according to the provided contracts.
        """
        intervals = Intervals([])
        for contract in contracts:
            if not contract.resource_calendar_id:
                # this field is not mandatory, so it can be null.
                continue
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
            intervals |= self._get_attendance_intervals_of_calendar(
                contract.resource_calendar_id,
                from_dt,
                to_dt,
            )
        return intervals

    def _get_attendance_intervals(self, from_datetime, to_datetime):
        from_datetime, to_datetime = self._localize_datetimes(
            from_datetime, to_datetime
        )
        contracts = self._get_active_contracts(from_datetime.date(), to_datetime.date())
        intervals = self._get_attendance_intervals_of_contracts(
            contracts, from_datetime, to_datetime
        )
        return intervals

    def _get_leave_intervals(self, from_datetime, to_datetime, domain):
        from_datetime, to_datetime = self._localize_datetimes(
            from_datetime, to_datetime
        )
        # leave intervals are stored in the calendar of the resource, which
        # should be the same as the one of the company.
        calendar = self.resource_calendar_id
        intervals = calendar._leave_intervals(
            from_datetime, to_datetime, self.resource_id, domain
        )
        return intervals

    def _get_work_intervals(self, from_datetime, to_datetime, domain):
        attendance_intervals = self._get_attendance_intervals(
            from_datetime, to_datetime
        )
        leave_intervals = self._get_leave_intervals(from_datetime, to_datetime, domain)
        return attendance_intervals - leave_intervals

    def _get_attendance_time_per_day(self, from_datetime, to_datetime):
        """
        Return the attendance time per day according to all contracts of the
        resource, ignoring leaves.
        """
        intervals = self._get_attendance_intervals(from_datetime, to_datetime)
        return self._sum_hours_per_date_from_intervals(intervals)

    def _localize_datetimes(self, from_datetime, to_datetime):
        # naive datetimes are considered utc
        if not from_datetime.tzinfo:
            from_datetime = from_datetime.replace(tzinfo=utc)
        if not to_datetime.tzinfo:
            to_datetime = to_datetime.replace(tzinfo=utc)

        tz = timezone(self.tz)
        return from_datetime.astimezone(tz), to_datetime.astimezone(tz)
