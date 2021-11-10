# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime
from collections import defaultdict

from odoo import fields, models


class ResourceMixin(models.AbstractModel):

    _inherit = "resource.mixin"

    # make this field read-only.
    resource_calendar_id = fields.Many2one("resource.calendar", readonly=True)

    def list_work_time_per_day(
        self, from_datetime, to_datetime, calendar=None, domain=None
    ):
        default_work_time = super().list_work_time_per_day(
            from_datetime, to_datetime, calendar, domain
        )
        if calendar or not hasattr(self, "contract_ids"):
            return default_work_time
        contracts = self._get_active_contracts(
            from_datetime.date(), to_datetime.date()
        )
        work_time_results = self._get_work_time_per_contract(
            contracts, from_datetime, to_datetime, domain
        )
        result = []
        for work_time_per_day in default_work_time:
            day = work_time_per_day[0]
            hours = 0.0
            for work_time in work_time_results:
                hours += work_time[day]
            result.append((day, hours))
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
        normal_work_time_per_day = super().list_work_time_per_day(
            from_datetime.replace(hour=0, minute=0, second=0),
            to_datetime.replace(hour=0, minute=0, second=0)
            + datetime.timedelta(days=1),
            calendar=None,
            domain=domain,
        )
        work_time_per_day = self.list_work_time_per_day(
            from_datetime, to_datetime, calendar=None, domain=domain
        )
        num_days = 0.0
        num_hours = 0.0
        for (_, work_time), (_, normal_work_time) in zip(
            work_time_per_day, normal_work_time_per_day
        ):
            if work_time == 0.0:
                continue
            num_days += work_time / normal_work_time
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
                    date_start.year, date_start.month, date_start.day
                )
            date_end = contract.date_end
            if date_end and to_dt.date() > date_end:
                # limit to midnight on the day after date_end to completely
                # include date_end.
                to_dt = datetime.datetime(
                    date_end.year, date_end.month, date_end.day
                ) + datetime.timedelta(days=1)
            work_time_results.append(
                defaultdict(
                    float,
                    super().list_work_time_per_day(
                        from_dt,
                        to_dt,
                        contract.resource_calendar_id,
                        domain,
                    ),
                )
            )
        return work_time_results
