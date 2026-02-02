# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import datetime

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval


class Partner(models.Model):
    _inherit = "res.partner"

    customer_wallet_balance = fields.Monetary(
        compute="_compute_customer_wallet",
        search="_search_customer_wallet_balance",
        recursive=True,
    )
    account_move_line_ids = fields.One2many(
        comodel_name="account.move.line",
        inverse_name="partner_id",
        readonly=True,
    )

    has_customer_wallet = fields.Boolean(compute="_compute_customer_wallet")

    customer_wallet_data = fields.Text(compute="_compute_customer_wallet")

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

    def get_wallet_balance_details(self, all_partner_ids, wallet_account_id):
        # We use sudo for account.move.line
        # to avoid access error, if user is not member of accouting groups

        result = {partner_id: [] for partner_id in all_partner_ids}
        domain = [
            ("partner_id", "in", list(all_partner_ids)),
            ("parent_state", "=", "posted"),
            ("account_id", "=", wallet_account_id.id),
        ]
        _fields = ["date", "create_date", "balance", "partner_id", "move_id"]

        for line in self.env["account.move.line"].sudo().search_read(domain, _fields):
            result[line["partner_id"][0]].append(
                {
                    "model": "account.move.line",
                    "partner_id": line["partner_id"][0],
                    "datetime": datetime.datetime(
                        line["date"].year, line["date"].month, line["date"].day
                    ),
                    "create_date": line["create_date"],
                    "amount": -line["balance"],
                    "reference": line["move_id"][1],
                }
            )

        return result

    def _customer_wallet_depends(self):
        return [
            "account_move_line_ids",
            "account_move_line_ids.account_id",
            "account_move_line_ids.balance",
            "account_move_line_ids.parent_state",
            "child_ids",
            "child_ids.customer_wallet_balance",
            "parent_id",
            "parent_id.customer_wallet_balance",
        ]

    @api.depends(lambda self: self._customer_wallet_depends())
    @api.depends_context("company")
    def _compute_customer_wallet(self):
        wallet_account_id = self.env.company.customer_wallet_account_id
        if not wallet_account_id or not self.ids:
            # Always assign a value in a compute method.
            self.write(
                {
                    "customer_wallet_balance": 0.0,
                    "customer_wallet_data": str([]),
                    "has_customer_wallet": False,
                }
            )
            return

        all_partner_families = {}
        all_partner_ids = set()

        # we split the calculation in two part to optimize it
        # because the call of get_all_partners_in_family take time
        # and is not necessary for most partners
        for partner in self.filtered(lambda x: x.parent_id or x.child_ids):
            all_partner_families[partner] = partner.get_all_partners_in_family()

        for partner in self.filtered(lambda x: not x.parent_id and not x.child_ids):
            all_partner_families[partner] = [partner.id]

        for val in all_partner_families.values():
            all_partner_ids |= set(val)

        all_totals = self.get_wallet_balance_details(all_partner_ids, wallet_account_id)

        for partner, child_ids in all_partner_families.items():
            lines = []
            for partner_id in child_ids:
                lines += all_totals.get(partner_id)

            partner.customer_wallet_balance = sum(line["amount"] for line in lines)
            lines.sort(key=lambda x: (x["datetime"], x["create_date"]))
            balance = 0
            for line in lines:
                balance += line["amount"]
                line["balance"] = balance
            partner.has_customer_wallet = len(lines)
            partner.customer_wallet_data = str(lines)

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
            return []
        else:
            # TODO maybe
            raise NotImplementedError()

    def action_view_customer_wallet_details(self):
        self.ensure_one()
        return {
            "name": _("Customer Wallet Details"),
            "view_mode": "form",
            "res_model": "customer.wallet.detail.wizard",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_partner_id": self.id},
        }

    def action_view_customer_wallet_redistribute(self):
        self.ensure_one()
        return {
            "name": _("Redistribute Customer Wallet"),
            "view_mode": "form",
            "res_model": "customer.wallet.redistribute.wizard",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_partner_id": self.id},
        }
