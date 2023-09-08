# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import api, models


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_wallet_balance_pos_payment(self, all_partner_ids):
        pre_result = defaultdict(float)
        for line in (
            self.env["pos.payment"]
            .sudo()
            .search(
                [
                    ("partner_id", "in", list(all_partner_ids)),
                    ("session_id.state", "=", "opened"),
                    ("pos_order_id.state", "=", "paid"),
                    ("payment_method_id.is_customer_wallet_method", "=", True),
                ]
            )
        ):
            pre_result[line.partner_id.id] += line.amount
        return [
            {"partner_id": partner_id, "total": total}
            for partner_id, total in pre_result.items()
        ]

    @api.model
    def get_wallet_balance_pos_order_line(self, all_partner_ids):
        pre_result = defaultdict(float)
        for line in (
            self.env["pos.order.line"]
            .sudo()
            .search(
                [
                    ("order_id.state", "=", "paid"),
                    ("order_id.partner_id", "in", list(all_partner_ids)),
                    ("product_id.is_customer_wallet_product", "=", True),
                ]
            )
        ):
            pre_result[line.order_id.partner_id.id] -= line.price_subtotal
        return [
            {"partner_id": partner_id, "total": total}
            for partner_id, total in pre_result.items()
        ]

    def get_wallet_balance_all(self, all_partner_ids, all_account_ids):
        res = super().get_wallet_balance_all(all_partner_ids, all_account_ids)
        res.append(self.get_wallet_balance_pos_order_line(all_partner_ids))
        res.append(self.get_wallet_balance_pos_payment(all_partner_ids))
        return res
