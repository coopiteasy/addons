# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CustomerWalletDetailWizardLine(models.TransientModel):
    _name = "customer.wallet.redistribute.wizard.line"
    _description = "Customer Wallet Redistribute Wizard Line"

    wizard_id = fields.Many2one(
        required=True,
        comodel_name="customer.wallet.redistribute.wizard",
        ondelete="cascade",
    )

    partner_id = fields.Many2one(required=True, comodel_name="res.partner")

    currency_id = fields.Many2one(
        comodel_name="res.currency", related="partner_id.currency_id"
    )

    amount = fields.Monetary(
        string="Amount to receive",
        required=True,
    )
