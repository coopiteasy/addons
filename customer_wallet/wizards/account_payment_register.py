# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    is_customer_wallet_journal = fields.Boolean(
        related="journal_id.is_customer_wallet_journal",
    )
    customer_wallet_balance = fields.Monetary(
        string="Customer Wallet Balance",
        currency_field="currency_id",
        related="partner_id.customer_wallet_balance",
    )
