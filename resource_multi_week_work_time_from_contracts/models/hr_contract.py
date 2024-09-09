# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    # Add a domain.
    resource_calendar_id = fields.Many2one(
        "resource.calendar",
        domain="[('parent_calendar_id', '=', False)]",
    )
