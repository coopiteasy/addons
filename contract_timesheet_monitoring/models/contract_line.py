from odoo import api, fields, models
from odoo.exceptions import UserError


class ContractLine(models.Model):
    _inherit = "contract.line"

    time_spent = fields.Float(
        string="Time Spent", compute="_compute_time_spent"
    )
    time_available = fields.Integer(related="product_id.time_available")

    time_remaining = fields.Float(
        string="Time Remaining", compute="_compute_time_remaining"
    )
    date_of_last_invoice = fields.Date(compute="_get_date_of_last_invoice")

    def _get_period_start_date(self):
        if self.recurring_invoicing_type == 'post-paid':
            start_date = self.recurring_next_dat
        else:
            start_date = self.recurring_next_date - self.get_relative_delta(
                            self.recurring_rule_type, self.recurring_interval
                        )
        return start_date

    @api.depends("analytic_account_id.line_ids")
    def _compute_time_spent(self):
        for line in self:
            if line.analytic_account_id:
                period_start_date = line._get_period_start_date()
                line.time_spent = line.analytic_account_id.get_time_spent_for_period(
                    period_start_date
                )
            else:
                line.time_spent = False

    @api.depends("time_available", "time_spent")
    def _compute_time_remaining(self):
        for line in self:
            line.time_remaining = line.time_available - line.time_spent
