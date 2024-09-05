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
            candidate = None
            days_to_monday = (7 - date_from.weekday()) % 7 or 7
            new_date_from = date_from
            # Keep searching the Mondays of succeeding weeks until a match is
            # found. Loop as many times as there are calendars.
            for _ in self.multi_week_calendar_ids:
                new_date_from = new_date_from + datetime.timedelta(days=days_to_monday)
                candidate = super(
                    ResourceCalendar, self._get_multi_week_calendar(new_date_from)
                )._get_first_attendance(new_date_from)
                if candidate:
                    break
                days_to_monday = 7
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
            candidate = None
            days_since_sunday = date_to.weekday() + 1
            new_date_to = date_to
            # Keep searching the Sundays of preceding weeks until a match is
            # found. Loop as many times as there are calendars.
            for _ in self.multi_week_calendar_ids:
                new_date_to = new_date_to - datetime.timedelta(days=days_since_sunday)
                candidate = super(
                    ResourceCalendar, self._get_multi_week_calendar(new_date_to)
                )._get_last_attendance(new_date_to)
                if candidate:
                    break
                days_since_sunday = 7
        return candidate
