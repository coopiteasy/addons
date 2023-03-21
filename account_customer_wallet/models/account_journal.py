# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    is_customer_wallet_journal = fields.Boolean(
        string="Customer Wallet Journal", default=False
    )

    minimum_wallet_amount = fields.Monetary(
        string="Minimum Wallet Amount",
        default=0.0,
        help="Usually 0. You can enter a negative value,"
        " if you want to accept that the customer wallet"
        " is negative. Maybe useful if the sale amount"
        " is slightly higher than the wallet amount,"
        " to avoid charging the customer a small amount.",
    )
