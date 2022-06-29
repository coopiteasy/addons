# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta, timezone

from .test_work_time_base import TestWorkTimeBase


class TestWorkDaysData(TestWorkTimeBase):
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
                "hours": 38.0,
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
                # this is 22.8, but writing 22.8 will cause a failure because
                # of floating-point precision.
                "hours": 7.6 * 3,
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
                "hours": 15.2,
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
                "name": "Contract 2",
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
                "hours": 38.0,
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
                "name": "Contract 2",
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
                "hours": 34.2,
            },
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
                "date_from": self.to_utc_datetime(2021, 10, 26, 8, 42),
                "date_to": self.to_utc_datetime(2021, 10, 26, 12, 30),
                "resource_id": self.employee1.resource_id.id,
                "time_type": "leave",
            }
        )
        self.env["resource.calendar.leaves"].create(
            {
                "name": "Wednesday afternoon",
                "calendar_id": self.employee1.resource_calendar_id.id,
                "date_from": self.to_utc_datetime(2021, 10, 27, 13, 30),
                "date_to": self.to_utc_datetime(2021, 10, 27, 17, 18),
                "resource_id": self.employee1.resource_id.id,
                "time_type": "leave",
            }
        )
        self.env["resource.calendar.leaves"].create(
            {
                "name": "Friday",
                "calendar_id": self.employee1.resource_calendar_id.id,
                "date_from": self.to_utc_datetime(2021, 10, 29, 8, 42),
                "date_to": self.to_utc_datetime(2021, 10, 29, 17, 18),
                "resource_id": self.employee1.resource_id.id,
                "time_type": "leave",
            }
        )
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 3.0,
                # this is 22.8, but writing 22.8 will cause a failure because
                # of floating-point precision.
                "hours": 7.6 * 3,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 25),
                self.local_datetime(2021, 11, 1),
                compute_leaves=False,
            ),
            {
                "days": 5.0,
                "hours": 38.0,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 12, 30),
            ),
            {
                "days": 0.0,
                "hours": 0.0,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 12, 30),
                compute_leaves=False,
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 13, 30),
                self.local_datetime(2021, 10, 26, 17, 18),
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 13, 30),
                self.local_datetime(2021, 10, 26, 17, 18),
                compute_leaves=False,
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 27, 8, 42),
                self.local_datetime(2021, 10, 27, 17, 18),
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 27, 8, 42),
                self.local_datetime(2021, 10, 27, 17, 18),
                compute_leaves=False,
            ),
            {
                "days": 1.0,
                "hours": 7.6,
            },
        )

    def test_precision(self):
        """
        Days should be rounded to the 1/16th.
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
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 8, 48),
            ),
            {
                "days": 0.0,
                "hours": 0.1,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 9, 6),
            ),
            {
                "days": 0.0625,
                "hours": 0.4,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 9, 18),
            ),
            {
                "days": 0.0625,
                "hours": 0.6,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 9, 36),
            ),
            {
                "days": 0.125,
                "hours": 0.9,
            },
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
                "date_from": self.to_utc_datetime(2021, 10, 26, 8, 42),
                "date_to": self.to_utc_datetime(2021, 10, 26, 9, 30),
                "resource_id": self.employee1.resource_id.id,
                "time_type": "leave",
            }
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 12, 30),
            ),
            {
                "days": 0.375,
                "hours": 3.0,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.local_datetime(2021, 10, 26, 8, 42),
                self.local_datetime(2021, 10, 26, 12, 30),
                compute_leaves=False,
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.to_utc_datetime(2021, 10, 26, 8, 42),
                self.to_utc_datetime(2021, 10, 26, 12, 30),
            ),
            {
                "days": 0.375,
                "hours": 3.0,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.to_utc_datetime(2021, 10, 26, 8, 42),
                self.to_utc_datetime(2021, 10, 26, 12, 30),
                compute_leaves=False,
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.to_utc_datetime(2021, 10, 26, 8, 42).replace(tzinfo=None),
                self.to_utc_datetime(2021, 10, 26, 12, 30).replace(tzinfo=None),
            ),
            {
                "days": 0.375,
                "hours": 3.0,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.to_utc_datetime(2021, 10, 26, 8, 42).replace(tzinfo=None),
                self.to_utc_datetime(2021, 10, 26, 12, 30).replace(tzinfo=None),
                compute_leaves=False,
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.to_utc_datetime(2021, 10, 26, 8, 42).astimezone(
                    timezone(timedelta(hours=23))
                ),
                self.to_utc_datetime(2021, 10, 26, 12, 30).astimezone(
                    timezone(timedelta(hours=-23))
                ),
            ),
            {
                "days": 0.375,
                "hours": 3.0,
            },
        )
        self.assertEqual(
            self.employee1.get_work_days_data(
                self.to_utc_datetime(2021, 10, 26, 8, 42).astimezone(
                    timezone(timedelta(hours=23))
                ),
                self.to_utc_datetime(2021, 10, 26, 12, 30).astimezone(
                    timezone(timedelta(hours=-23))
                ),
                compute_leaves=False,
            ),
            {
                "days": 0.5,
                "hours": 3.8,
            },
        )

    def _get_employee_work_days(self):
        from_datetime = self.local_datetime(2021, 10, 25)
        to_datetime = from_datetime + timedelta(days=7)
        return self.employee1.get_work_days_data(from_datetime, to_datetime)
