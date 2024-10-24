from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def get_time_spent_for_period(self, start_date, end_date=None):
        analytic_account_lines = self.line_ids
        timesheets = analytic_account_lines.filtered(
            # keep only timesheets
            # ensure the uom is the same as the one configure for the project
            # timesheets (hours or day)
            lambda x: (x.product_uom_id.measure_type == "time")
        )
        if timesheets:
            time_spent_on_account = timesheets.filtered(
                lambda x: (x.date >= start_date)
            ).mapped("unit_amount")
            return sum(time_spent_on_account)
