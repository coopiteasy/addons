# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta, timezone

from odoo.tests.common import users

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
                "date_end": "2021-10-26",
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
        # 4.5 days because on the 2021-10-25 (monday), only one day is counted
        # because the morning attendances overlap and only the total time is
        # counted. 0.5 comes from the morning of 2021-10-26 (tuesday).
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 4.5,
                "hours": 34.2,
            },
        )

    def test_short_days(self):
        """
        Shorter days should be counted as a full days.
        """
        calendar = self.env["resource.calendar"].create(
            {"name": "4 * 4.47", "attendance_ids": False}
        )
        for day in range(4):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 10,
                    "hour_to": 14.75,
                    "calendar_id": calendar.id,
                }
            )
        calendar._onchange_hours_per_day()
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": calendar.id,
                "date_start": "2020-10-24",
            }
        )
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 4,
                "hours": 19,
            },
        )

    def test_irregular_days(self):
        """
        Half days in contracts should be counted as a half days.
        """
        calendar = self.env["resource.calendar"].create(
            {"name": "Nine tenth", "attendance_ids": False}
        )
        for day in (0, 2, 3, 4):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 8.7,
                    "hour_to": 12.5,
                    "calendar_id": calendar.id,
                }
            )
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 13.5,
                    "hour_to": 17.3,
                    "calendar_id": calendar.id,
                }
            )
        self.env["resource.calendar.attendance"].create(
            {
                "name": "Attendance",
                "dayofweek": "1",
                "hour_from": 8.7,
                "hour_to": 12.5,
                "calendar_id": calendar.id,
            }
        )
        # this must be forced to set the default day length.
        calendar.hours_per_day = 7.6
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": calendar.id,
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

    @users("user1")
    def test_access_rights(self):
        """
        Should be able to be run from an employee user with no access rights
        to contracts.
        """
        # here sudo() is needed only to create the contract.
        self.env["hr.contract"].sudo().create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.full_time_calendar.id,
                "date_start": "2020-10-24",
            }
        )
        # this is needed to reload the record, otherwise it has superuser
        # access rights.
        self.employee1 = self.env["hr.employee"].browse(self.employee1.id)
        self.assertEqual(
            self._get_employee_work_days(),
            {
                "days": 5.0,
                "hours": 38.0,
            },
        )

    def _get_employee_work_days(self):
        from_datetime = self.local_datetime(2021, 10, 25)
        to_datetime = from_datetime + timedelta(days=7)
        return self.employee1.get_work_days_data(from_datetime, to_datetime)
