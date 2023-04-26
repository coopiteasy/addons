# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        if not soft:
            partners = self.env["res.partner"]
            for partner in self.mapped("line_ids.partner_id"):
                partners |= partner.get_all_partners_in_family()
            partners._compute_customer_wallet_balance()
        return res
