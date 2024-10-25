# Copyright 2016 Tecnativa - Carlos Dauden
# Copyright 2018 ACSONE SA/NV.
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    time_spent = fields.Float(
        string="Time Spent", compute="_compute_time_spent"
    )
    time_available = fields.Integer(related="product_id.time_available")
    
    time_remaining = fields.Float(
        string="Time Remaining", compute="_compute_time_remaining"
    )

    @api.depends("account_analytic_id.line_ids")
    def _compute_time_spent(self):
        for line in self:
            if line.account_analytic_id and line.start_date:
                 line.time_spent = line.account_analytic_id.get_time_spent_for_period(
                    line.start_date, line.end_date
                )
            else:
                line.time_spent = False

    @api.depends("time_available", "time_spent")
    def _compute_time_remaining(self):
        for line in self:
            line.time_remaining = line.time_available - line.time_spent
