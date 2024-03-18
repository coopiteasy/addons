# Copyright 2016 Tecnativa - Carlos Dauden
# Copyright 2018 ACSONE SA/NV.
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    time_spent = fields.Float(
        string="Time Spent this Period", compute="_compute_time_spent"
    )

    def get_time_spent(self, analytic_distribution, start_date, end_date=None):
        total_time_spent = 0
        for analytic_account, percentage in analytic_distribution.items():
            analytic_account_id = int(analytic_account)
            analytic_account_lines = (
                self.env["account.analytic.account"]
                .browse(analytic_account_id)
                .line_ids
            )
            timesheets = analytic_account_lines.filtered(
                # keep only timesheets
                # ensure the uom is the same as the one configure for the project
                # timesheets (hours or day)
                lambda x: (x.encoding_uom_id == x.project_id.timesheet_encode_uom_id)
            )
            if timesheets:
                time_spent_on_account = timesheets.filtered(
                    lambda x: (x.date >= start_date)
                ).mapped("unit_amount")
                total_time_spent_on_account = sum(time_spent_on_account)
                total_time_spent += total_time_spent_on_account * percentage / 100
        return total_time_spent

    def _compute_time_spent(self):
        for line in self:
            if line.analytic_distribution and line.start_date:
                line.time_spent = line.get_time_spent(
                    line.analytic_distribution, line.start_date
                )
            else:
                line.time_spent = False
