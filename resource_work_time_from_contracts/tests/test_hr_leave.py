# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from .test_work_time_base import TestWorkTimeBase


class TestHrLeave(TestWorkTimeBase):
    def setUp(self):
        super().setUp()

        self.leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Dummy leave type",
                "allocation_type": "no",
                "validity_start": "2020-10-24",
            }
        )

    def test_get_request_attendances_multiple_contracts(self):
        """
        The correct attendances should be returned, even with overlapping
        contracts that have attendances outside of their validity date range.
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.afternoon_calendar.id,
                "date_start": "2020-10-24",
                "date_end": "2021-10-26",
            }
        )
        self.env["hr.contract"].create(
            {
                "name": "Contract 2",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.morning_calendar.id,
                "date_start": "2021-10-26",
            }
        )
        leave = self.env["hr.leave"].create(
            {
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee1.id,
                "request_date_from": "2021-10-25",
                "request_date_to": "2021-10-27",
            }
        )
        leave._onchange_request_parameters()
        self.assertEqual(
            leave.date_from,
            self.to_utc_datetime(2021, 10, 25, 13, 30).replace(tzinfo=None),
        )
        self.assertEqual(
            leave.date_to,
            self.to_utc_datetime(2021, 10, 27, 12, 30).replace(tzinfo=None),
        )

    def test_get_request_attendances_multiple_weeks(self):
        """
        The correct attendances should be returned, even with contracts with
        no attendances on the requested days and when the date range spans
        multiple weeks.
        """
        calendar = self.env["resource.calendar"].create(
            {"name": "Dummy calendar", "attendance_ids": False}
        )
        self.env["resource.calendar.attendance"].create(
            {
                "name": "Attendance",
                "dayofweek": "3",
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
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": calendar.id,
                "date_start": "2020-10-24",
            }
        )
        leave = self.env["hr.leave"].create(
            {
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee1.id,
                "request_date_from": "2021-10-20",
                "request_date_to": "2021-10-27",
            }
        )
        leave._onchange_request_parameters()
        self.assertEqual(
            leave.date_from,
            self.to_utc_datetime(2021, 10, 20, 13, 30).replace(tzinfo=None),
        )
        self.assertEqual(
            leave.date_to,
            self.to_utc_datetime(2021, 10, 27, 12, 30).replace(tzinfo=None),
        )

    def test_get_request_attendances_multiple_weeks_no_match_found(self):
        """
        With contracts with no matching attendances, default attendances
        should be returned.
        """
        calendar = self.env["resource.calendar"].create(
            {"name": "Dummy calendar", "attendance_ids": False}
        )
        self.env["resource.calendar.attendance"].create(
            {
                "name": "Attendance",
                "dayofweek": "1",
                "hour_from": 13.5,
                "hour_to": 17.3,
                "calendar_id": calendar.id,
            }
        )
        self.env["resource.calendar.attendance"].create(
            {
                "name": "Attendance",
                "dayofweek": "2",
                "hour_from": 8.7,
                "hour_to": 12.5,
                "calendar_id": calendar.id,
            }
        )
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": calendar.id,
                "date_start": "2020-10-24",
            }
        )
        leave = self.env["hr.leave"].create(
            {
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee1.id,
                "request_date_from": "2021-10-21",
                "request_date_to": "2021-10-25",
            }
        )
        leave._onchange_request_parameters()
        self.assertEqual(
            leave.date_from, self.to_utc_datetime(2021, 10, 21).replace(tzinfo=None)
        )
        self.assertEqual(
            leave.date_to, self.to_utc_datetime(2021, 10, 25).replace(tzinfo=None)
        )

    def test_get_request_attendances_no_contracts(self):
        """
        Without contracts, attendances from the employee's resource calendar
        should be returned.
        """
        self.employee1.resource_calendar_id = self.full_time_calendar
        leave = self.env["hr.leave"].create(
            {
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee1.id,
                "request_date_from": "2021-10-25",
                "request_date_to": "2021-10-27",
            }
        )
        leave._onchange_request_parameters()
        self.assertEqual(
            leave.date_from,
            self.to_utc_datetime(2021, 10, 25, 8, 42).replace(tzinfo=None),
        )
        self.assertEqual(
            leave.date_to,
            self.to_utc_datetime(2021, 10, 27, 17, 18).replace(tzinfo=None),
        )

    def test_get_request_attendances_no_contracts_empty_calendar(self):
        """
        Without contracts and with no attendances in the employee's resource
        calendar, default attendances should be returned.
        """
        leave = self.env["hr.leave"].create(
            {
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee1.id,
                "request_date_from": "2021-10-25",
                "request_date_to": "2021-10-27",
            }
        )
        leave._onchange_request_parameters()
        self.assertEqual(
            leave.date_from, self.to_utc_datetime(2021, 10, 25).replace(tzinfo=None)
        )
        self.assertEqual(
            leave.date_to, self.to_utc_datetime(2021, 10, 27).replace(tzinfo=None)
        )

    def test_get_request_attendances_no_match(self):
        """
        Without valid contracts, default attendances should be returned.
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.full_time_calendar.id,
                "date_start": "2020-10-24",
                "date_end": "2021-10-23",
            }
        )
        leave = self.env["hr.leave"].create(
            {
                "holiday_status_id": self.leave_type.id,
                "employee_id": self.employee1.id,
                "request_date_from": "2021-10-25",
                "request_date_to": "2021-10-27",
            }
        )
        leave._onchange_request_parameters()
        self.assertEqual(
            leave.date_from, self.to_utc_datetime(2021, 10, 25).replace(tzinfo=None)
        )
        self.assertEqual(
            leave.date_to, self.to_utc_datetime(2021, 10, 27).replace(tzinfo=None)
        )
