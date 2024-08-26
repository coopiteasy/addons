# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from odoo import models


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    def get_first_last_attendance(self, date_from, date_to):
        """
        Get the first and last attendances between (and including) date_from
        and date_to.

        Return 2 tuples of the form (date, attendance). Each of the tuples can
        be None if there is no match.
        """
        # we should get the first attendance from a list of all the
        # attendances that starts with the weekday of date_from then wraps
        # around and ends with the weekday before date_from. the list should
        # be no longer (in terms of weekdays) than date_to - date_from + 1.
        all_attendances = self.attendance_ids
        if not all_attendances:
            return (None, None)
        weekday_from = date_from.weekday()
        weekday_to = date_to.weekday()
        all_attendances = all_attendances.filtered(
            lambda r: int(r.dayofweek) >= weekday_from
        ) + all_attendances.filtered(lambda r: int(r.dayofweek) < weekday_from)
        first_attendance = all_attendances[0]
        weekday_diff = int(first_attendance.dayofweek) - weekday_from
        if weekday_diff < 0:
            weekday_diff += 7
        first_attendance_date = date_from + datetime.timedelta(days=weekday_diff)
        if first_attendance_date > date_to:
            first_attendance_tuple = None
        else:
            first_attendance_tuple = (first_attendance_date, first_attendance)
        # do the same (but in the other direction) for date_to
        all_attendances = self.attendance_ids
        all_attendances = all_attendances.filtered(
            lambda r: int(r.dayofweek) > weekday_to
        ) + all_attendances.filtered(lambda r: int(r.dayofweek) <= weekday_to)
        last_attendance = all_attendances[-1]
        weekday_diff = int(last_attendance.dayofweek) - weekday_to
        if weekday_diff > 0:
            weekday_diff -= 7
        last_attendance_date = date_to + datetime.timedelta(days=weekday_diff)
        if last_attendance_date < date_from:
            last_attendance_tuple = None
        else:
            last_attendance_tuple = (last_attendance_date, last_attendance)
        return (first_attendance_tuple, last_attendance_tuple)
