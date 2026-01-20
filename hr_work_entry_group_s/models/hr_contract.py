# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    group_s_code = fields.Char(default=None)
