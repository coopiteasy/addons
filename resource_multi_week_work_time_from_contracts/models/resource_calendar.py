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
            ResourceCalendar, self._get_calendar(date_from)
        )._get_first_attendance(date_from)
        # Week numbers not equal. This means we are AFTER any of the attendances
        # in the target week. So get the first attendance of the succeeding
        # week.
        #
        # TODO: This implementation assumes that the calendar is populated with
        # at least one attendance.
        if candidate and candidate[0].isocalendar()[1] != date_from.isocalendar()[1]:
            days_to_monday = (7 - date_from.weekday()) % 7
            next_monday = (date_from + datetime.timedelta(days=days_to_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            candidate = super(
                ResourceCalendar, self._get_calendar(next_monday)
            )._get_first_attendance(next_monday)
        return candidate

    def _get_last_attendance(self, date_to):
        if not self.is_multi_week:
            return super()._get_last_attendance(date_to)
        candidate = super(
            ResourceCalendar, self._get_calendar(date_to)
        )._get_last_attendance(date_to)
        # Week numbers not equal. This means we are BEFORE any of the
        # attendances in the target week. So get the last attendance of the
        # preceding week.
        #
        # TODO: This implementation assumes that the calendar is populated with
        # at least one attendance.
        if candidate and candidate[0].isocalendar()[1] != date_to.isocalendar()[1]:
            days_since_sunday = date_to.weekday() + 1
            last_sunday = (
                date_to - datetime.timedelta(days=days_since_sunday)
            ).replace(hour=23, minute=59, second=59, microsecond=99999)
            candidate = super(
                ResourceCalendar, self._get_calendar(last_sunday)
            )._get_last_attendance(last_sunday)
        return candidate
