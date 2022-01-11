# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"
    _order = "line_count desc"

    line_count = fields.Integer(
        string="Line Count", compute="_compute_line_count", store=True
    )

    @api.depends("line_ids")
    @api.multi
    def _compute_line_count(self):
        # may lead to performance issues. See with time.
        for account in self:
            one_month_ago = date.today() - timedelta(days=30)
            recent_lines = account.line_ids.filtered(
                lambda l: l.date >= one_month_ago
            )
            account.line_count = len(recent_lines)

    @api.model
    def cron_compute_line_count(self):
        accounts = self.search([])
        accounts._compute_line_count()
