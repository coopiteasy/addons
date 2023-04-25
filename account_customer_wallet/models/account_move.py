# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        if not soft:
            partners = self.mapped("line_ids.partner_id")
            partners |= partners.mapped("child_ids")
            partners |= partners.mapped("parent_id")
            partners._compute_customer_wallet_balance()
        return res
