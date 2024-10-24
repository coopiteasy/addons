# Copyright 2016 Tecnativa - Carlos Dauden
# Copyright 2018 ACSONE SA/NV.
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    time_spent = fields.Float(
        string="Time Spent", compute="_compute_time_spent"
    )
    time_available = fields.Integer(related="product_id.hours_available")



    def _compute_time_spent(self):
        for line in self:
            if line.analytic_account and line.start_date:
                 line.time_spent = line.analytic_account_id.get_time_spent_for_period(
                    line.start_date, line.end_date
                )
            else:
                line.time_spent = False
