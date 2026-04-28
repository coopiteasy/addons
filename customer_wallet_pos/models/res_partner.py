# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import models


class Partner(models.Model):
    _inherit = "res.partner"

    def _customer_wallet_depends(self):
        res = super()._customer_wallet_depends()
        res += [
            "pos_order_ids.lines.product_id",
            "pos_order_ids.payment_ids",
        ]
        return res

    def get_wallet_balance_details(self, all_partner_ids, all_account_ids):
        # We use sudo for pos.payment and pos.order.line
        # to avoid access error, if user is not member of point of sale groups
        result = super().get_wallet_balance_details(all_partner_ids, all_account_ids)

        # Manage Pending Pos Order Lines
        domain = [
            ("order_id.partner_id", "in", list(all_partner_ids)),
            ("order_id.state", "=", "paid"),
            ("product_id.is_customer_wallet_product", "=", True),
        ]

        for order_line in self.env["pos.order.line"].sudo().search(domain):
            result[order_line.order_id.partner_id.id].append(
                {
                    "model": "pos.order.line",
                    "partner_id": order_line.order_id.partner_id.id,
                    "datetime": order_line.create_date,
                    "create_date": order_line.create_date,
                    "amount": order_line.price_subtotal,
                    "reference": order_line.order_id.name,
                }
            )
        # manage Pending Pos Payments
        domain = [
            ("partner_id", "in", list(all_partner_ids)),
            ("pos_order_id.state", "=", "paid"),
            ("payment_method_id.is_customer_wallet_method", "=", True),
        ]
        _fields = [
            "create_date",
            "payment_date",
            "amount",
            "partner_id",
            "pos_order_id",
        ]

        for line in self.env["pos.payment"].sudo().search_read(domain, _fields):
            result[line["partner_id"][0]].append(
                {
                    "model": "pos.payment",
                    "partner_id": line["partner_id"][0],
                    "datetime": line["payment_date"],
                    "create_date": line["create_date"],
                    "amount": -line["amount"],
                    "reference": line["pos_order_id"][1],
                }
            )

        return result
