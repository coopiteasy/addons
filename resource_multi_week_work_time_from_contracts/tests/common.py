# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import SavepointCase


class TestCalendarCommon(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Calendar = cls.env["resource.calendar"]
        cls.parent_calendar = cls.Calendar.create(
            {
                "name": "Parent",
                # This date is a Monday.
                "multi_week_epoch_date": "2024-07-08",
            }
        )
        cls.child_1 = cls.Calendar.create(
            {
                "name": "Child 1",
                "parent_calendar_id": cls.parent_calendar.id,
                "week_sequence": 10,
                "attendance_ids": [
                    (
                        0,
                        False,
                        {
                            "name": "Wednesday morning",
                            "dayofweek": "2",
                            "hour_from": 8,
                            "hour_to": 12,
                        },
                    ),
                    (
                        0,
                        False,
                        {
                            "name": "Thursday morning",
                            "dayofweek": "3",
                            "hour_from": 8,
                            "hour_to": 12,
                        },
                    ),
                ],
            }
        )
        cls.child_2 = cls.Calendar.create(
            {
                "name": "Child 2",
                "parent_calendar_id": cls.parent_calendar.id,
                "week_sequence": 20,
                "attendance_ids": [
                    (
                        0,
                        False,
                        {
                            "name": "Monday morning",
                            "dayofweek": "0",
                            "hour_from": 8,
                            "hour_to": 12,
                        },
                    ),
                    (
                        0,
                        False,
                        {
                            "name": "Friday morning",
                            "dayofweek": "4",
                            "hour_from": 8,
                            "hour_to": 12,
                        },
                    ),
                ],
            }
        )
