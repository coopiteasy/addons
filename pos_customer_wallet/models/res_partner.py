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
        # Note the current algorithm could not work in a multi company
        # context, for partner shared in many companies.
        # TODO : ask to carmen how `_where_calc` works, and how to make
        # join.
        query = """
            SELECT sum(pol.price_subtotal) as total, po.partner_id
            FROM pos_order_line pol
            INNER JOIN pos_order po on pol.order_id = po.id
            INNER JOIN product_product pp on pol.product_id = pp.id
            INNER JOIN product_template pt on pp.product_tmpl_id = pt.id
            WHERE po.state = 'paid'
            AND pt.is_customer_wallet_product = true
            AND po.partner_id in %s
            GROUP BY po.partner_id;
            """
        self.env.cr.execute(query, (tuple(all_partner_ids),))
        return self.env.cr.dictfetchall()

    def _compute_customer_wallet_balance(self):
        super()._compute_customer_wallet_balance()

        if not self.ids:
            return True

        all_partner_families = {}
        all_partner_ids = set()
        for partner in self:
            all_partner_families[partner] = partner.get_all_partners_in_family()
            all_partner_ids |= set(all_partner_families[partner])

        if not all_partner_ids:
            return True

        statement_line_totals = self.get_wallet_balance_bank_statement_line(
            all_partner_ids
        )
        order_line_totals = self.get_wallet_balance_pos_order_line(all_partner_ids)
        for partner, child_ids in all_partner_families.items():
            partner.customer_wallet_balance += sum(
                -total["total"]
                for total in statement_line_totals
                if total["partner_id"] in child_ids
            ) + sum(
                total["total"]
                for total in order_line_totals
                if total["partner_id"] in child_ids
            )
