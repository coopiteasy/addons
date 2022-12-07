# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class MailActivitySummary(models.Model):
    _name = "mail.activity.summary"

    name = fields.Char(string="Name", required=True)
