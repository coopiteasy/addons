# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models

from odoo.addons.hr_holidays.models.hr_leave import DummyAttendance


class HrLeave(models.Model):
    _inherit = "hr.leave"

    # in hr_holidays, this method reads the resource.calendar.attendance
    # records directly from the employee's or company resource.calendar to
    # find the first one and the last one corresponding to the leave date
    # range. this overrides this behavior.
    def _get_attendances(self, employee, request_date_from, request_date_to):
        """
        Get the first and last resource.calendar.attendance corresponding to
        the range defined by request_date_from and request_date_to.
        """
        attendance_from, attendance_to = employee.get_attendances_of_date_range(
            request_date_from, request_date_to
        )
        default_value = DummyAttendance(0, 0, 0, "morning", False)
        if attendance_from is None:
            attendance_from = default_value
        if attendance_to is None:
            attendance_to = default_value
        return attendance_from, attendance_to
