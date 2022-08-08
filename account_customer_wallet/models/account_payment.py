# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    is_customer_wallet_journal = fields.Boolean(
        related="journal_id.is_customer_wallet_journal",
    )

    customer_wallet_balance = fields.Monetary(
        string="Customer Wallet Balance",
        currency_field="currency_id",
        related="partner_id.customer_wallet_balance",
    )

    @api.multi
    def post(self):
        wallet_payments = self.filtered(
            lambda x: x.journal_id.is_customer_wallet_journal
        )

        for payment in wallet_payments:
            if payment.partner_id and payment.customer_wallet_balance < payment.amount:
                raise UserError(
                    _(
                        "There is not enough balance in the customer's wallet"
                        " to perform this payment. \n"
                        " - Customer : %s\n"
                        " - Customer Wallet : %s\n"
                        " - Amount Payment : %s"
                    )
                    % (
                        payment.partner_id.display_name,
                        payment.customer_wallet_balance,
                        payment.amount,
                    )
                )
        return super().post()
