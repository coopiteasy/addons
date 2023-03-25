# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestBalance(SavepointCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.partner = cls.env.ref("base.res_partner_address_30")
        cls.sale_product = cls.env.ref("product.product_product_4d")
        cls.customer_wallet_account = cls.env.ref(
            "account_customer_wallet.account_account_customer_wallet_demo"
        )
        cls.sale_account = cls.env["account.account"].search(
            [
                (
                    "user_type_id.id",
                    "=",
                    cls.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        cls.customer_wallet_journal = cls.env.ref(
            "account_customer_wallet.account_journal_customer_wallet_demo"
        )
        cls.sale_journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        cls.payment_method = cls.env.ref("account.account_payment_method_manual_in")
        cls.cash_account = cls.env["account.account"].search(
            [("user_type_id.type", "=", "liquidity")], limit=1
        )
        cls.company_id = cls.env.user.company_id

    def _create_move(self, debit=0, credit=0, partner=None):
        if partner is None:
            partner = self.partner

        self.env["account.move"].create(
            {
                "journal_id": self.customer_wallet_journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "debit": debit,
                            "credit": credit,
                            "partner_id": partner.id,
                            "account_id": self.customer_wallet_account.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "debit": credit,
                            "credit": debit,
                            "partner_id": partner.id,
                            "account_id": self.cash_account.id,
                        },
                    ),
                ],
            }
        )

    def _create_sale_invoice(self, invoice_type, amount, partner=None):
        if partner is None:
            partner = self.partner
        invoice = self.env["account.invoice"].create(
            {
                "journal_id": self.sale_journal.id,
                "type": invoice_type,
                "partner_id": partner.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Invoice line",
                            "quantity": 1,
                            "price_unit": amount,
                            "product_id": self.sale_product.id,
                            "account_id": self.sale_account.id,
                        },
                    )
                ],
            }
        )
        invoice.action_invoice_open()
        return invoice

    def _create_payment(self, invoice, amount=0, partner=None):
        if partner is None:
            partner = self.partner

        payment = (
            self.env["account.payment"]
            .with_context(
                active_model="account.invoice",
                active_ids=invoice.ids,
            )
            .create(
                {
                    "amount": amount,
                    "journal_id": self.customer_wallet_journal.id,
                    "payment_method_id": self.payment_method.id,
                }
            )
        )
        payment.post()
