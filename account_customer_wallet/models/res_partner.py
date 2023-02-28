# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class Partner(models.Model):
    _inherit = "res.partner"

    customer_wallet_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.customer_wallet_account_id",
        readonly=True,
    )
    customer_wallet_balance = fields.Monetary(
        string="Customer Wallet Balance",
        compute="_compute_customer_wallet_balance",
        readonly=True,
        search="_search_customer_wallet_balance",
    )

    def get_topmost_parent_id(self):
        self.ensure_one()
        if not self.parent_id:
            return self
        return self.parent_id.get_topmost_parent_id()

    def get_all_partners_in_family(self):
        self.ensure_one()
        return (
            self.with_context(active_test=False)
            .search([("id", "child_of", self.get_topmost_parent_id().id)])
            .ids
        )

    def get_wallet_balance_account_move_line(self, all_partner_ids, all_account_ids):
        account_move_line = self.env["account.move.line"]
        # generate where clause to include multicompany rules
        where_query = account_move_line._where_calc(
            [
                ("partner_id", "in", list(all_partner_ids)),
                # TODO: Filter on state?
                # ("state", "not in", ["draft", "cancel"]),
                # FIXME: This should ideally be something like
                # `("account_id", "=", partner.customer_wallet_account_id)`,
                # but that may not be possible.
                ("account_id", "in", list(all_account_ids)),
            ]
        )
        account_move_line._apply_ir_rules(where_query, "read")
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        # balance is in the company currency
        query = (
            """
            SELECT SUM(balance) as total, partner_id
            FROM account_move_line account_move_line
            WHERE %s
            GROUP BY partner_id
            """
            % where_clause
        )
        self.env.cr.execute(query, where_clause_params)
        return self.env.cr.dictfetchall()

    def _compute_customer_wallet_balance(self):
        if not self.ids:
            return True

        all_partner_families = {}
        all_partner_ids = set()
        all_account_ids = set()
        for partner in self:
            all_partner_families[partner] = partner.get_all_partners_in_family()
            all_partner_ids |= set(all_partner_families[partner])
            all_account_ids.add(partner.customer_wallet_account_id.id)

        move_line_totals = self.get_wallet_balance_account_move_line(
            all_partner_ids, all_account_ids
        )

        for partner, child_ids in all_partner_families.items():
            partner.customer_wallet_balance = sum(
                -total["total"]
                for total in move_line_totals
                if total["partner_id"] in child_ids
            )

    def _search_customer_wallet_balance(self, operator, value):
        # This is a complete and utter hack. Don't do what I did.
        if operator in ("=", "!=", ">", ">=", "<", "<=", "=?", "in", "not in"):
            if operator in ("=", "=?"):
                operator = "=="
            filter_string = "partner.customer_wallet_balance {operator} {value}".format(
                operator=operator, value=value
            )
            filtered = self.search([]).filtered(
                lambda partner: safe_eval(
                    filter_string,
                    {"partner": partner},
                )
            )
            if filtered:
                return [("id", "in", [partner.id for partner in filtered])]
        else:
            # TODO maybe
            raise NotImplementedError()
