# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models

from odoo.addons.hr_holidays.models.hr_leave import DummyAttendance


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _get_request_attendances(self):
        """
        Get the first and last resource.calendar.attendance corresponding to
        the range defined by request_date_from and request_date_to.
        """
        attendance_from, attendance_to = self.employee_id.get_attendances_of_date_range(
            self.request_date_from, self.request_date_to
        )
        default_value = DummyAttendance(0, 0, 0, "morning")
        if attendance_from is None:
            attendance_from = default_value
        if attendance_to is None:
            attendance_to = default_value
        return attendance_from, attendance_to
