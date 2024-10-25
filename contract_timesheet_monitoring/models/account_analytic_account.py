from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def get_time_spent_for_period(self, start_date, end_date=None):
        analytic_account_lines = self.line_ids
        timesheets = analytic_account_lines.filtered(
            # keep only timesheets
            lambda x: (x.product_uom_id.measure_type == "time")
        )
        if timesheets:
            if start_date:
                timesheets = timesheets.filtered(
                    lambda x: (x.date >= start_date)
                )
            return sum(timesheets.mapped("unit_amount"))
