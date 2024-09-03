# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

import pytz

from .common import TestCalendarCommon


class TestWorkTime(TestCalendarCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.timezone = pytz.timezone(cls.env.user.tz)

        cls.user1 = cls.env["res.users"].create(
            {
                "name": "User 1",
                "login": "user1",
                "password": "user1",
                "groups_id": [(6, 0, cls.env.ref("base.group_user").ids)],
            }
        )

        cls.employee1 = cls.env["hr.employee"].create(
            {
                "name": "Employee 1",
                "user_id": cls.user1.id,
                "address_id": cls.user1.partner_id.id,
            }
        )

    def local_datetime(self, year, month, day, *args, **kwargs):
        """
        Create a datetime with the local timezone from local time values
        """
        return self.timezone.localize(
            datetime.datetime(year, month, day, *args, **kwargs)
        )

    def test_single_contract(self):
        """A very rudimentary test that checks whether the glue module works. It
        does not test any corner cases.
        """
        self.env["hr.contract"].create(
            {
                "name": "Contract 1",
                "employee_id": self.employee1.id,
                "wage": 0.0,
                "resource_calendar_id": self.parent_calendar.id,
                "date_start": "2020-10-18",
            }
        )
        self.assertEqual(
            self.employee1.list_work_time_per_day(
                self.local_datetime(2024, 7, 8), self.local_datetime(2024, 7, 21)
            ),
            [
                (datetime.date(2024, 7, 10), 4),
                (datetime.date(2024, 7, 11), 4),
                (datetime.date(2024, 7, 15), 4),
                (datetime.date(2024, 7, 19), 4),
            ],
        )
