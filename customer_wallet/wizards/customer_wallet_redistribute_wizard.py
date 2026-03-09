# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


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

    amount = fields.Monetary(
        compute="_compute_amount",
        readonly=False,
        string="Amount to distribute",
        required=True,
    )

    line_ids = fields.One2many(
        comodel_name="customer.wallet.redistribute.wizard.line",
        inverse_name="wizard_id",
    )

    def _default_journal_id(self):
        return self.env.company.customer_wallet_redistribution_journal_id

    @api.depends("partner_id")
    def _compute_amount(self):
        for wizard in self:
            wizard.amount = wizard.partner_id.customer_wallet_balance

    def button_redistribute(self):
        self.ensure_one()

        wallet_account_id = self.env.company.customer_wallet_account_id.id
        total_amount = sum(self.mapped("line_ids.amount"))

        if self.amount <= 0:
            raise UserError(
                _("The amount to redistribute should be strictly positive.")
            )

        if self.amount != total_amount:
            raise UserError(
                _(
                    "The amount to be redistributed (%(amount)s) is"
                    " different from the sum of the amounts (%(total_amount)s).",
                    amount=self.amount,
                    total_amount=total_amount,
                )
            )

        if len(self.mapped("line_ids.partner_id").ids) != len(self.mapped("line_ids")):
            raise UserError(_("you cannot select the same beneficiary twice."))

        if self.partner_id.id in self.mapped("line_ids.partner_id").ids:
            raise UserError(
                _(
                    "The redistributor customer is included in the list of beneficiaries."
                )
            )

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

        line_vals = [
            Command.create(
                {
                    "debit": self.amount,
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
                "journal_id": journals[0].id,
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
