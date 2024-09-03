# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    def _get_first_attendance(self, date_from):
        if not self.is_multi_week:
            return super()._get_first_attendance(date_from)
        return super(
            ResourceCalendar, self._get_calendar(date_from)
        )._get_first_attendance(date_from)

    def _get_last_attendance(self, date_to):
        if not self.is_multi_week:
            return super()._get_last_attendance(date_to)
        return super(
            ResourceCalendar, self._get_calendar(date_to)
        )._get_last_attendance(date_to)
