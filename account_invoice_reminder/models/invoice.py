from odoo import fields, models


class account_invoice(models.Model):
    _inherit = "account.invoice"

    reminder = fields.Selection(
        [
            ("1", "First reminder"),
            ("2", "Second reminder"),
            ("3", "Third reminder"),
            ("4", "Registered mail"),
        ],
        string="Reminder",
    )
    last_reminder_date = fields.Date(string="Date of last reminder")
