# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from .test_work_time_base import TestWorkTimeBase


class TestWorkDaysData(TestWorkTimeBase):
    def setUp(self):
        super().setUp()
        self.company_calendar = self.env["resource.calendar"].create(
            {"name": "Company", "attendance_ids": False}
        )
        # the company calendar must contain full-time days
        for day in range(7):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "08",
                    "hour_to": "12",
                    "calendar_id": self.company_calendar.id,
                }
            )
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "13",
                    "hour_to": "17",
                    "calendar_id": self.company_calendar.id,
                }
            )
        self.employee1.company_id.resource_calendar_id = self.company_calendar

    def test_no_contract(self):
        """
        Work days for an employee without a contract should be 0
        """
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 0.0,
                "hours": 0.0,
            },
        )

    def test_single_contract(self):
        """
        Single contract
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.full_time_calendar.id,
                "date_start": "2020-10-24",
            }
        )
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 5.0,
                "hours": 40.0,
            },
        )

    def test_single_contract_with_start_date(self):
        """
        Single contract with a start date in range
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.full_time_calendar.id,
                "date_start": "2021-10-27",
            }
        )
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 3.0,
                "hours": 24.0,
            },
        )

    def test_single_contract_with_end_date(self):
        """
        Single contract with an end date
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.full_time_calendar.id,
                "date_start": "2020-10-24",
                "date_end": "2021-10-26",
            }
        )
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 2.0,
                "hours": 16.0,
            },
        )

    def test_multiple_contracts(self):
        """
        Multiple simultaneous contracts
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.morning_calendar.id,
                "date_start": "2020-10-24",
            }
        )
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.afternoon_calendar.id,
                "date_start": "2020-10-24",
            }
        )
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 5.0,
                "hours": 40.0,
            },
        )

    def test_multiple_contracts_with_dates(self):
        """
        Multiple overlapping contracts with dates
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.morning_calendar.id,
                "date_start": "2020-10-24",
                "date_end": "2021-10-25",
            }
        )
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.four_fifths_calendar.id,
                "date_start": "2020-10-24",
            }
        )
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 4.5,
                "hours": 36.0,
            },
        )

    def _get_employee_work_days(self):
        from_datetime = datetime(2021, 10, 25)
        to_datetime = from_datetime + timedelta(days=7)
        return self.employee1.get_work_days_data(from_datetime, to_datetime)
