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

    # this method is a duplicate from get_time_spent in contract.line
    # but this is due to the fact that contract line tend to mimic account move lines
    # it make sense to keep these methods separated.
    def get_time_spent(self, analytic_distribution, start_date, end_date=None):
        total_time_spent = 0
        for analytic_account, percentage in analytic_distribution.items():
            analytic_account = self.env["account.analytic.account"].browse(
                int(analytic_account)
            )
            time_spent_on_account = analytic_account.get_time_spent_for_period(
                start_date
            )
            total_time_spent += time_spent_on_account * percentage / 100
        return total_time_spent

    def _compute_time_spent(self):
        for line in self:
            if line.analytic_distribution and line.start_date:
                line.time_spent = line.get_time_spent(
                    line.analytic_distribution, line.start_date, line.end_date
                )
            else:
                line.time_spent = False
