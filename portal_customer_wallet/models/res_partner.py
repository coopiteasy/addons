# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections import defaultdict

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def customer_wallet_payments_per_month(self):
        """Return a dictionary with (year, month) keys. The value is the amount
        spent using the customer wallet for every month.
        """
        self.ensure_one()
        # Like in account_customer_wallet, search against all partners in family.
        all_partners_in_family = self.get_all_partners_in_family()
        wallet_account_id = self.env.company.customer_wallet_account_id
        move_lines = self.env["account.move.line"].search(
            [
                ("partner_id", "in", all_partners_in_family),
                ("account_id", "=", wallet_account_id.id),
                # Negative balances = fill up the customer wallet. We're only
                # interested in customer wallet spendings here, so let's skip
                # them.
                ("balance", ">", 0),
            ]
        )
        per_month_dict = defaultdict(int)
        for move_line in move_lines:
            date = move_line.move_id.date
            per_month_dict[(date.year, date.month)] += move_line.balance
        return per_month_dict
