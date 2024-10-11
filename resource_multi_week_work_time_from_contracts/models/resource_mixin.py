# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ResourceMixing(models.AbstractModel):
    _inherit = "resource.mixin"

    def get_calendar_for_date(self, date):
        calendar = super().get_calendar_for_date(date)
        if calendar is not None:
            calendar = calendar._get_multi_week_calendar(day=date)
        return calendar
