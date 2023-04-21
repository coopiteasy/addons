# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBalance(TransactionCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.partner_parent = cls.env["res.partner"].create(
            {"name": "Test Partner Parent", "company_id": cls.env.company.id}
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "company_id": cls.env.company.id,
                "parent_id": cls.partner_parent.id,
            }
        )
        template = cls.env["product.template"].create(
            {"name": "Sale Product Test", "standard_price": 500}
        )
        cls.sale_product = template.product_variant_id
        cls.customer_wallet_account = cls.env.ref(
            "account_customer_wallet.account_account_customer_wallet_demo"
        )
        cls.sale_account = cls.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "income",
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
            [("account_type", "=", "asset_cash")], limit=1
        )
        cls.company_id = cls.env.company

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
        invoice = self.env["account.move"].create(
            {
                "journal_id": self.sale_journal.id,
                "move_type": invoice_type,
                "partner_id": partner.id,
                "line_ids": [
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
        invoice.action_post()
        return invoice

    def _create_payment(self, invoice, amount=0, partner=None):
        if partner is None:
            partner = self.partner
        register = (
            self.env["account.payment.register"]
            .with_context(
                active_model="account.move",
                active_ids=invoice.ids,
            )
            .create(
                {
                    "journal_id": self.customer_wallet_journal.id,
                }
            )
        )
        return register._create_payments()
