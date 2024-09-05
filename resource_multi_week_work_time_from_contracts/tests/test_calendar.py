# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from .common import TestCalendarCommon


class TestCalendar(TestCalendarCommon):
    def test_first_last_attendance_both_weeks(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.date.fromisoformat("2024-07-08"),
            datetime.date.fromisoformat("2024-07-21"),
        )
        # First date/attendance is the Wednesday.
        self.assertEqual(result[0][0], datetime.date.fromisoformat("2024-07-10"))
        self.assertEqual(result[0][1], self.child_1.attendance_ids[0])
        # Last date/attendance is the Friday.
        self.assertEqual(result[1][0], datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[-1])

    def test_first_last_attendance_middle_to_middle(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.date.fromisoformat("2024-07-11"),
            datetime.date.fromisoformat("2024-07-16"),
        )
        # First date/attendance is the Thursday.
        self.assertEqual(result[0][0], datetime.date.fromisoformat("2024-07-11"))
        self.assertEqual(result[0][1], self.child_1.attendance_ids[1])
        # Last date/attendance is the Monday.
        self.assertEqual(result[1][0], datetime.date.fromisoformat("2024-07-15"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[0])

    def test_first_last_attendance_middle_to_before(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.date.fromisoformat("2024-07-16"),
            datetime.date.fromisoformat("2024-07-22"),
        )
        # First date/attendance is the Friday.
        self.assertEqual(result[0][0], datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[0][1], self.child_2.attendance_ids[1])
        # Last date/attendance is the Friday of the week preceding the target date.
        self.assertEqual(result[1][0], datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[1])

    def test_first_last_attendance_middle_to_before_skip_a_week(self):
        self.Calendar.create(
            {
                "name": "Empty child 3",
                "parent_calendar_id": self.parent_calendar.id,
                "week_sequence": 30,  # After week 2.
                "attendance_ids": [],
            }
        )
        result = self.parent_calendar.get_first_last_attendance(
            # Multi-week 2
            datetime.date.fromisoformat("2024-07-16"),
            # Multi-week 1
            datetime.date.fromisoformat("2024-07-30"),
        )
        # First date/attendance is the Friday.
        self.assertEqual(result[0][0], datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[0][1], self.child_2.attendance_ids[1])
        # Last date/attendance is the Friday of the second week preceding the
        # target date.
        self.assertEqual(result[1][0], datetime.date.fromisoformat("2024-07-19"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[1])

    def test_first_last_attendance_after_to_middle(self):
        result = self.parent_calendar.get_first_last_attendance(
            datetime.date.fromisoformat("2024-07-12"),
            datetime.date.fromisoformat("2024-07-17"),
        )
        # First date/attendance is the Monday of the week succeeding the target date.
        self.assertEqual(result[0][0], datetime.date.fromisoformat("2024-07-15"))
        self.assertEqual(result[0][1], self.child_2.attendance_ids[0])
        # Last date/attendance is the Monday.
        self.assertEqual(result[1][0], datetime.date.fromisoformat("2024-07-15"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[0])

    def test_first_last_attendance_after_to_middle_skip_a_week(self):
        self.Calendar.create(
            {
                "name": "Empty child 3",
                "parent_calendar_id": self.parent_calendar.id,
                # In between week 1 and 2, meaning child 2 is now week 3.
                "week_sequence": 15,
                "attendance_ids": [],
            }
        )
        result = self.parent_calendar.get_first_last_attendance(
            # Multi-week 1.
            datetime.date.fromisoformat("2024-07-12"),
            # Multi-week 3.
            datetime.date.fromisoformat("2024-07-24"),
        )
        # First date/attendance is the Monday of the second week succeeding the
        # target date.
        self.assertEqual(result[0][0], datetime.date.fromisoformat("2024-07-22"))
        self.assertEqual(result[0][1], self.child_2.attendance_ids[0])
        # Last date/attendance is the Monday.
        self.assertEqual(result[1][0], datetime.date.fromisoformat("2024-07-22"))
        self.assertEqual(result[1][1], self.child_2.attendance_ids[0])
