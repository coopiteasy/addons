# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, datetime, timedelta

from .test_work_time_base import TestWorkTimeBase


class TestWorkTime(TestWorkTimeBase):
    def test_no_contract(self):
        """
        Work time for an employee without a contract should be 0
        """
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 0.0),
                (date(2021, 10, 20), 0.0),
            ],
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
                "date_start": "2020-10-18",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 8.0),
                (date(2021, 10, 20), 8.0),
            ],
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
                "date_start": "2021-10-20",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 0.0),
                (date(2021, 10, 20), 8.0),
            ],
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
                "date_start": "2020-10-18",
                "date_end": "2021-10-19",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 8.0),
                (date(2021, 10, 20), 0.0),
            ],
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
                "date_start": "2020-10-18",
            }
        )
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.afternoon_calendar.id,
                "date_start": "2020-10-18",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 8.0),
                (date(2021, 10, 20), 8.0),
            ],
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
                "date_start": "2020-10-18",
                "date_end": "2021-10-19",
            }
        )
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.four_fifths_calendar.id,
                "date_start": "2020-10-19",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 4.0),
                (date(2021, 10, 20), 8.0),
            ],
        )

    def _get_employee_work_time(self):
        from_datetime = datetime(2021, 10, 19)
        to_datetime = from_datetime + timedelta(days=2)
        return self.employee1.list_work_time_per_day(
            from_datetime, to_datetime
        )
