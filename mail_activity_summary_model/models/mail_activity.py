# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    summary = fields.Char(compute="_compute_summary", inverse="_inverse_summary")
    summary_id = fields.Many2one(
        comodel_name="mail.activity.summary",
        string="Summary",
        ondelete="set null",
    )

    @api.depends("summary_id", "summary_id.name")
    def _compute_summary(self):
        for record in self:
            if record.summary_id:
                record.summary = record.summary_id.name
            else:
                record.summary = False

    def _inverse_summary(self):
        for record in self:
            if not record.summary:
                record.summary_id = None
            else:
                summary_id = self.env["mail.activity.summary"].search(
                    [("name", "=", record.summary)],
                    limit=1,
                )
                if not summary_id:
                    summary_id = self.env["mail.activity.summary"].create(
                        {"name": record.summary}
                    )
                record.summary_id = summary_id
