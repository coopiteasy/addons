# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class Partner(models.Model):
    _inherit = "res.partner"

    customer_wallet_balance = fields.Monetary(
        compute="_compute_customer_wallet_balance",
        search="_search_customer_wallet_balance",
    )

    def get_topmost_parent_id(self):
        self.ensure_one()
        if not self.parent_id:
            return self
        return self.parent_id.get_topmost_parent_id()

    def get_all_partners_in_family(self):
        self.ensure_one()
        return self.with_context(active_test=False).search(
            [("id", "child_of", self.get_topmost_parent_id().id)]
        )

    def get_wallet_balance_account_move_line(self, all_partner_ids, wallet_account_id):
        pre_result = defaultdict(float)
        for line in (
            self.env["account.move.line"]
            .sudo()
            .search(
                [
                    ("partner_id", "in", list(all_partner_ids)),
                    # Check state
                    ("parent_state", "=", "posted"),
                    # FIXME: This should ideally be something like
                    # `("account_id", "=", partner.customer_wallet_account_id)`,
                    # but that may not be possible.
                    ("account_id", "=", wallet_account_id.id),
                ]
            )
        ):
            pre_result[line.partner_id.id] += line.balance
        return [
            {"partner_id": partner_id, "total": total}
            for partner_id, total in pre_result.items()
        ]

    def get_wallet_balance_all(self, all_partner_ids, wallet_account_id):
        # Overload in other modules (like pos_customer_wallet)
        return [
            self.get_wallet_balance_account_move_line(
                all_partner_ids, wallet_account_id
            )
        ]

    @api.depends_context("company")
    def _compute_customer_wallet_balance(self):
        if not self.ids:
            return True

        all_partner_families = {}
        all_partner_ids = set()
        wallet_account_id = self.env.company.customer_wallet_account_id
        if not wallet_account_id:
            # No wallet account defined in the current context
            for partner in self:
                partner.customer_wallet_balance = 0.0
            return

        # we split the calculation in two part to optimize it
        # because the call of get_all_partners_in_family take time
        # and is not necessary for most partners
        for partner in self.filtered(lambda x: x.parent_id or x.child_ids):
            all_partner_families[partner] = partner.get_all_partners_in_family().ids
            all_partner_ids |= set(all_partner_families[partner])

        for partner in self.filtered(lambda x: not x.parent_id and not x.child_ids):
            all_partner_families[partner] = [partner.id]
            all_partner_ids |= set(all_partner_families[partner])

        all_totals = self.get_wallet_balance_all(all_partner_ids, wallet_account_id)

        for partner, child_ids in all_partner_families.items():
            wallet_balance = 0.0
            for totals in all_totals:
                wallet_balance += sum(
                    -total["total"]
                    for total in totals
                    if total["partner_id"] in child_ids
                )
            partner.customer_wallet_balance = wallet_balance

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
