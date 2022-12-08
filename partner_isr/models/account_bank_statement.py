# Copyright 2019 Coop IT Easy SC
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.multi
    def set_partner_on_bank_statement_line(self):
        self.ensure_one()
        if self.state == "open":
            customers = self.env["res.partner"].search(
                [("customer", "=", True), ("isr_number", "!=", False)]
            )
            for line in self.line_ids:
                partner = customers.filtered(
                    lambda cust: cust.isr_number == line.ref.lstrip("0")
                )
                if partner:
                    line.partner_id = partner.id
