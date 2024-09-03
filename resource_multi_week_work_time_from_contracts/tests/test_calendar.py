# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from .common import TestCalendarCommon


class TestCalendar(TestCalendarCommon):
    def test_first_last_attendance_both_weeks(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.datetime.fromisoformat("2024-07-08T00:00:00+00:00"),
            datetime.datetime.fromisoformat("2024-07-21T23:59:59+00:00"),
        )
        # First date/attendance is the Wednesday.
        self.assertEqual(result[0][0].date(), datetime.date.fromisoformat("2024-07-10"))
        self.assertEqual(result[0][1], self.child_1.attendance_ids[0])
        # Last date/attendance is the Friday.
        self.assertEqual(result[1][0].date(), datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[-1])

    def test_first_last_attendance_middle_to_middle(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.datetime.fromisoformat("2024-07-11T00:00:00+00:00"),
            datetime.datetime.fromisoformat("2024-07-16T23:59:59+00:00"),
        )
        # First date/attendance is the Thursday.
        self.assertEqual(result[0][0].date(), datetime.date.fromisoformat("2024-07-11"))
        self.assertEqual(result[0][1], self.child_1.attendance_ids[1])
        # Last date/attendance is the Monday.
        self.assertEqual(result[1][0].date(), datetime.date.fromisoformat("2024-07-15"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[0])

    def test_first_last_attendance_middle_to_before(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.datetime.fromisoformat("2024-07-16T00:00:00+00:00"),
            datetime.datetime.fromisoformat("2024-07-22T23:59:59+00:00"),
        )
        # First date/attendance is the Friday.
        self.assertEqual(result[0][0].date(), datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[0][1], self.child_2.attendance_ids[1])
        # Last date/attendance is the Friday of the week preceding the target date.
        self.assertEqual(result[1][0].date(), datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[1])

    def test_first_last_attendance_after_to_middle(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.datetime.fromisoformat("2024-07-12T00:00:00+00:00"),
            datetime.datetime.fromisoformat("2024-07-17T23:59:59+00:00"),
        )
        # First date/attendance is the Monday of the week succeeding the target date.
        self.assertEqual(result[0][0].date(), datetime.date.fromisoformat("2024-07-15"))
        self.assertEqual(result[0][1], self.child_2.attendance_ids[0])
        # Last date/attendance is the Monday.
        self.assertEqual(result[1][0].date(), datetime.date.fromisoformat("2024-07-15"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[0])
