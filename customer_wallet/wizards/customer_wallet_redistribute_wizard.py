# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command, _, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_amount


class CustomerWalletRedistributeWizard(models.TransientModel):
    _name = "customer.wallet.redistribute.wizard"
    _description = "Customer Wallet Redistribute Wizard"

    partner_id = fields.Many2one(required=True, comodel_name="res.partner")

    currency_id = fields.Many2one(
        comodel_name="res.currency", related="partner_id.currency_id"
    )

    customer_wallet_balance = fields.Monetary(
        related="partner_id.customer_wallet_balance",
        string="Balance",
    )

    line_ids = fields.One2many(
        comodel_name="customer.wallet.redistribute.wizard.line",
        inverse_name="wizard_id",
    )

    def button_redistribute(self):
        self.ensure_one()

        wallet_account_id = self.env.company.customer_wallet_account_id.id

        journals = self.env["account.journal"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("is_customer_wallet_journal", "=", True),
            ]
        )
        if not journals:
            raise UserError(
                _("There no 'Wallet' journal defined. Please configure one first.")
            )
        wallet_journal = journals[0]

        total_amount = sum(self.mapped("line_ids.amount"))
        if (
            self.customer_wallet_balance - total_amount
        ) < wallet_journal.minimum_wallet_amount:
            raise UserError(
                _(
                    "The new balance (%(new_balance)s) is"
                    " lower than the minimum defined in the journal (%(minimum_amount)s).",
                    new_balance=format_amount(
                        self.self.customer_wallet_balance - total_amount,
                        self.currency_id,
                    ),
                    minimum_amount=format_amount(
                        wallet_journal.minimum_wallet_amount, self.currency_id
                    ),
                )
            )

        if not len(self.line_ids):
            raise UserError(_("Please set one or many lines."))

        if len(self.line_ids.partner_id) != len(self.line_ids):
            raise UserError(_("you cannot select the same beneficiary twice."))

        if self.partner_id in self.line_ids.partner_id:
            raise UserError(
                _(
                    "The redistributor customer is included in the list of beneficiaries."
                )
            )

        line_vals = [
            Command.create(
                {
                    "debit": total_amount,
                    "partner_id": self.partner_id.id,
                    "account_id": wallet_account_id,
                    "name": _("Customer Wallet Redistribution"),
                }
            )
        ]

        for line in self.line_ids:
            vals = {
                "credit": line.amount,
                "partner_id": line.partner_id.id,
                "account_id": wallet_account_id,
                "name": _(
                    "Customer Wallet. Receipt from %(partner_name)s",
                    partner_name=self.partner_id.name,
                ),
            }
            line_vals.append(Command.create(vals))

        move = self.env["account.move"].create(
            {
                "line_ids": line_vals,
                "journal_id": wallet_journal.id,
            }
        )
        move.action_post()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_journal_line"
        )
        action.update(
            {
                "res_id": move.id,
                "views": [(self.env.ref("account.view_move_form").id, "form")],
            }
        )
        return action
