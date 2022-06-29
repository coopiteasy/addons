# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta, timezone

from .test_work_time_base import TestWorkTimeBase


class TestWorkTime(TestWorkTimeBase):
    def test_no_contract(self):
        """
        Work time for an employee without a contract should be 0
        """
        self.assertEqual(self._get_employee_work_time(), [])

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
                (date(2021, 10, 19), 7.6),
                (date(2021, 10, 20), 7.6),
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
            [(date(2021, 10, 20), 7.6)],
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
            [(date(2021, 10, 19), 7.6)],
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
                "name": "Contract 2",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.afternoon_calendar.id,
                "date_start": "2020-10-18",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 7.6),
                (date(2021, 10, 20), 7.6),
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
                "name": "Contract 2",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.four_fifths_calendar.id,
                "date_start": "2020-10-19",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 3.8),
                (date(2021, 10, 20), 7.6),
            ],
        )

    def test_with_leaves(self):
        """
        Existing leaves should by default be subtracted from the work time
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

        self.env["resource.calendar.leaves"].create(
            {
                "name": "Tuesday morning",
                "calendar_id": self.employee1.resource_calendar_id.id,
                "date_from": self.to_utc_datetime(2021, 10, 19, 8, 42),
                "date_to": self.to_utc_datetime(2021, 10, 19, 12, 30),
                "resource_id": self.employee1.resource_id.id,
                "time_type": "leave",
            }
        )
        self.env["resource.calendar.leaves"].create(
            {
                "name": "Wednesday",
                "calendar_id": self.employee1.resource_calendar_id.id,
                "date_from": self.to_utc_datetime(2021, 10, 20, 8, 42),
                "date_to": self.to_utc_datetime(2021, 10, 20, 17, 18),
                "resource_id": self.employee1.resource_id.id,
                "time_type": "leave",
            }
        )
        self.assertEqual(
            self._get_employee_work_time(),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.local_datetime(2021, 10, 19, 8, 42),
                self.local_datetime(2021, 10, 19, 12, 30),
            ),
            [],
        )
        self.assertEqual(
            self.employee1.list_normal_work_time_per_day(
                self.local_datetime(2021, 10, 19, 8, 42),
                self.local_datetime(2021, 10, 19, 12, 30),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.local_datetime(2021, 10, 19, 13, 30),
                self.local_datetime(2021, 10, 19, 17, 18),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_normal_work_time_per_day(
                self.local_datetime(2021, 10, 19, 13, 30),
                self.local_datetime(2021, 10, 19, 17, 18),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.local_datetime(2021, 10, 19, 8, 42),
                self.local_datetime(2021, 10, 19, 17, 18),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_normal_work_time_per_day(
                self.local_datetime(2021, 10, 19, 8, 42),
                self.local_datetime(2021, 10, 19, 17, 18),
            ),
            [
                (date(2021, 10, 19), 7.6),
            ],
        )

    def test_timezone(self):
        """
        It should take the timezone into account.
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
        self.env["resource.calendar.leaves"].create(
            {
                "name": "Leave",
                "calendar_id": self.employee1.resource_calendar_id.id,
                "date_from": self.to_utc_datetime(2021, 10, 19, 8, 42),
                "date_to": self.to_utc_datetime(2021, 10, 19, 9, 30),
                "resource_id": self.employee1.resource_id.id,
                "time_type": "leave",
            }
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.local_datetime(2021, 10, 19, 8, 42),
                self.local_datetime(2021, 10, 19, 12, 30),
            ),
            [
                (date(2021, 10, 19), 3.0),
            ],
        )
        self.assertEqual(
            self.employee1.list_normal_work_time_per_day(
                self.local_datetime(2021, 10, 19, 8, 42),
                self.local_datetime(2021, 10, 19, 12, 30),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.to_utc_datetime(2021, 10, 19, 8, 42),
                self.to_utc_datetime(2021, 10, 19, 12, 30),
            ),
            [
                (date(2021, 10, 19), 3.0),
            ],
        )
        self.assertEqual(
            self.employee1.list_normal_work_time_per_day(
                self.to_utc_datetime(2021, 10, 19, 8, 42),
                self.to_utc_datetime(2021, 10, 19, 12, 30),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.to_utc_datetime(2021, 10, 19, 8, 42).replace(tzinfo=None),
                self.to_utc_datetime(2021, 10, 19, 12, 30).replace(tzinfo=None),
            ),
            [
                (date(2021, 10, 19), 3.0),
            ],
        )
        self.assertEqual(
            self.employee1.list_normal_work_time_per_day(
                self.to_utc_datetime(2021, 10, 19, 8, 42).replace(tzinfo=None),
                self.to_utc_datetime(2021, 10, 19, 12, 30).replace(tzinfo=None),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.to_utc_datetime(2021, 10, 19, 8, 42).astimezone(
                    timezone(timedelta(hours=23))
                ),
                self.to_utc_datetime(2021, 10, 19, 12, 30).astimezone(
                    timezone(timedelta(hours=-23))
                ),
            ),
            [
                (date(2021, 10, 19), 3.0),
            ],
        )
        self.assertEqual(
            self.employee1.list_normal_work_time_per_day(
                self.to_utc_datetime(2021, 10, 19, 8, 42).astimezone(
                    timezone(timedelta(hours=23))
                ),
                self.to_utc_datetime(2021, 10, 19, 12, 30).astimezone(
                    timezone(timedelta(hours=-23))
                ),
            ),
            [
                (date(2021, 10, 19), 3.8),
            ],
        )

    def _get_employee_work_time(self):
        from_datetime = self.local_datetime(2021, 10, 19)
        to_datetime = from_datetime + timedelta(days=2)
        return self.employee1.list_work_time_per_day(from_datetime, to_datetime)
