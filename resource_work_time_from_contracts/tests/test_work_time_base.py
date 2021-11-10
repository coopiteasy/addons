# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestWorkTimeBase(TransactionCase):
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
                    "hour_from": "08",
                    "hour_to": "12",
                    "calendar_id": self.full_time_calendar.id,
                }
            )
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "13",
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
                    "hour_from": "08",
                    "hour_to": "12",
                    "calendar_id": self.four_fifths_calendar.id,
                }
            )
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "13",
                    "hour_to": "17",
                    "calendar_id": self.four_fifths_calendar.id,
                }
            )
