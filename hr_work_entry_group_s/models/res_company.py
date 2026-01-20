# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    social_secretariat_affiliation_number = fields.Integer()
    group_s_report_counter = fields.Integer("Group S Report Sequence Number")

    def increment_group_s_report_counter(self):
        self.group_s_report_counter += 1
