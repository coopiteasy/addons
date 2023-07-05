# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_wallet_balance_bank_statement_line(self, all_partner_ids):
        account_bank_statement_line = self.env["account.bank.statement.line"].sudo()
        # generate where clause to include multicompany rules
        where_query = account_bank_statement_line._where_calc(
            [
                ("partner_id", "in", list(all_partner_ids)),
                ("state", "=", "open"),
                ("statement_id.journal_id.is_customer_wallet_journal", "=", True),
            ]
        )
        account_bank_statement_line._apply_ir_rules(where_query, "read")
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        # amount is in the company currency
        query = (
            """
            SELECT SUM(amount) as total, partner_id
            FROM account_bank_statement_line account_bank_statement_line
            WHERE %s
            GROUP BY partner_id
            """
            % where_clause
        )
        self.env.cr.execute(query, where_clause_params)
        return self.env.cr.dictfetchall()

    @api.model
    def get_wallet_balance_pos_order_line(self, all_partner_ids):
        # Suspend security because some users can not be member of
        # 'point of sale / user' group
        order_lines = (
            self.env["pos.order.line"]
            .sudo()
            .search(
                [
                    ("order_id.state", "=", "paid"),
                    ("order_id.partner_id", "in", list(all_partner_ids)),
                    ("product_id.is_customer_wallet_product", "=", True),
                ]
            )
        )
        if not order_lines:
            return []

        query = """
            SELECT - SUM(pol.price_subtotal) as total, po.partner_id
            FROM pos_order_line pol
            INNER JOIN pos_order po ON pol.order_id = po.id
            WHERE pol.id in %s
            GROUP BY po.partner_id
            """
        self.env.cr.execute(query, (tuple(order_lines.ids),))
        return self.env.cr.dictfetchall()

    def get_wallet_balance_all(self, all_partner_ids, all_account_ids):
        res = super().get_wallet_balance_all(all_partner_ids, all_account_ids)
        res.append(self.get_wallet_balance_bank_statement_line(all_partner_ids))
        res.append(self.get_wallet_balance_pos_order_line(all_partner_ids))
        return res
