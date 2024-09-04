# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from odoo import models


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    def _get_first_attendance(self, date_from):
        if not self.is_multi_week:
            return super()._get_first_attendance(date_from)
        candidate = super(
            ResourceCalendar, self._get_multi_week_calendar(date_from)
        )._get_first_attendance(date_from)
        # Week numbers not equal. This means we are AFTER any of the attendances
        # in the target week. So get the first attendance of the succeeding
        # week.
        if candidate and candidate[0].isocalendar()[1] != date_from.isocalendar()[1]:
            candidate = False
            next_monday = date_from
            # Keep searching succeeding weeks until a match is found. Loop as
            # many times as there are calendars.
            for _ in self.multi_week_calendar_ids:
                days_to_monday = (7 - next_monday.weekday()) % 7 or 7
                next_monday = (
                    next_monday + datetime.timedelta(days=days_to_monday)
                ).replace(hour=0, minute=0, second=0, microsecond=0)
                candidate = super(
                    ResourceCalendar, self._get_multi_week_calendar(next_monday)
                )._get_first_attendance(next_monday)
                if candidate:
                    break
        return candidate

    def _get_last_attendance(self, date_to):
        if not self.is_multi_week:
            return super()._get_last_attendance(date_to)
        candidate = super(
            ResourceCalendar, self._get_multi_week_calendar(date_to)
        )._get_last_attendance(date_to)
        # Week numbers not equal. This means we are BEFORE any of the
        # attendances in the target week. So get the last attendance of the
        # preceding week.
        if candidate and candidate[0].isocalendar()[1] != date_to.isocalendar()[1]:
            candidate = False
            last_sunday = date_to
            # Keep searching preceding weeks until a match is found. Loop as
            # many times as there are calendars.
            for _ in self.multi_week_calendar_ids:
                days_since_sunday = last_sunday.weekday() + 1
                last_sunday = (
                    last_sunday - datetime.timedelta(days=days_since_sunday)
                ).replace(hour=23, minute=59, second=59, microsecond=99999)
                candidate = super(
                    ResourceCalendar, self._get_multi_week_calendar(last_sunday)
                )._get_last_attendance(last_sunday)
                if candidate:
                    break
        return candidate
