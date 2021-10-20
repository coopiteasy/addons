# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, datetime, timedelta

from odoo.tests.common import TransactionCase


class TestWorkTime(TransactionCase):
    def setUp(self):
        super().setUp()

        # users
        user1_dict = {"name": "User 1", "login": "user1", "password": "user1"}
        self.user1 = self.env["res.users"].create(user1_dict)

        # employees
        employee1_dict = {
            "name": "Employee 1",
            "user_id": self.user1.id,
            "address_id": self.user1.partner_id.id,
        }
        self.employee1 = self.env["hr.employee"].create(employee1_dict)

        # working hours
        # calendar have default attendance_ids, force it to have none.
        self.full_time_calendar = self.env["resource.calendar"].create(
            {"name": "Full-time", "attendance_ids": False}
        )
        for day in range(5):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "09",
                    "hour_to": "17",
                    "calendar_id": self.full_time_calendar.id,
                }
            )

        self.morning_calendar = self.env["resource.calendar"].create(
            {"name": "Morning", "attendance_ids": False}
        )
        for day in range(5):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "08",
                    "hour_to": "12",
                    "calendar_id": self.morning_calendar.id,
                }
            )

        self.afternoon_calendar = self.env["resource.calendar"].create(
            {"name": "Afternoon", "attendance_ids": False}
        )
        for day in range(5):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "13",
                    "hour_to": "17",
                    "calendar_id": self.afternoon_calendar.id,
                }
            )

        self.four_fifths_calendar = self.env["resource.calendar"].create(
            {"name": "Four fifth", "attendance_ids": False}
        )
        for day in (0, 2, 3, 4):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "09",
                    "hour_to": "17",
                    "calendar_id": self.four_fifths_calendar.id,
                }
            )

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
