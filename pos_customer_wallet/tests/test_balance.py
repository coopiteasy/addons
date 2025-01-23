# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.fields import Command

from .common import TestPosBalance as TestBalance


class TestPosBalance(TestBalance):
    def test_with_pos_payment(self):
        """Pos payments in open POS sessions affect balance."""
        self._create_move(credit=100)
        self.create_wallet_pos_payment(amount=40)

        self.assertEqual(self.partner.customer_wallet_balance, 60)

    def test_with_pos_payment_different_partner(self):
        """Payments for other partners do not affect the balances of all
        clients.
        """
        other_partner = self.env.ref("base.res_partner_address_31")
        self.create_wallet_pos_payment(amount=100, partner=other_partner)

        self.assertEqual(self.partner.customer_wallet_balance, 0)
        self.assertEqual(other_partner.customer_wallet_balance, -100)

    def test_credit_by_product(self):
        # Intialize wallet with 500
        self._create_move(credit=500)

        self.create_wallet_pos_payment(
            product=self.wallet_product,
            payment_method=self.cash_payment_method,
            amount=1000,
        )
        self.assertEqual(self.partner.customer_wallet_balance, 1500)

    def test_close_session(self):
        """When closing a session, a correct account move is made."""
        self.create_wallet_pos_payment(
            amount=40,
            product=self.wallet_product,
            payment_method=self.cash_payment_method,
        )

        other_partner = self.env.ref("base.res_partner_address_31")
        self.create_wallet_pos_payment(
            amount=20,
            product=self.wallet_product,
            payment_method=self.cash_payment_method,
            partner=other_partner,
        )

        self.pos_session.action_pos_session_close()

        self.assertEqual(self.partner.customer_wallet_balance, 40)
        self.assertEqual(other_partner.customer_wallet_balance, 20)

        move_lines = self.env["account.move.line"].search(
            [
                ("partner_id", "in", (self.partner | other_partner).ids),
                (
                    "account_id",
                    "=",
                    self.customer_wallet_account.id,
                ),
            ]
        )
        # One line for each partner
        self.assertEqual(len(move_lines), 2)
        # Two credits and one debit on the move
        self.assertEqual(len(move_lines[0].move_id.line_ids), 3)
        # Credit amount is correct
        self.assertEqual(
            move_lines.filtered(lambda line: line.partner_id == self.partner).credit,
            40,
        )

    def test_close_session_buy_negative_product(self):
        """When buying a negatively priced wallet product, decrease balance."""
        self.create_wallet_pos_payment(
            amount=-40,
            product=self.wallet_product,
            payment_method=self.cash_payment_method,
        )
        self.pos_session.action_pos_session_close()

        self.assertEqual(self.partner.customer_wallet_balance, -40)


class TestTaxes(TestBalance):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def create_tag(name):
            return cls.env["account.account.tag"].create(
                {
                    "name": name,
                    "applicability": "taxes",
                    "country_id": cls.env.company.account_fiscal_country_id.id,
                }
            )

        cls.tax_tag_invoice_base = create_tag("Invoice Base tag")
        cls.tax_tag_invoice_tax = create_tag("Invoice Tax tag")
        cls.tax_tag_refund_base = create_tag("Refund Base tag")
        cls.tax_tag_refund_tax = create_tag("Refund Tax tag")
        cls.tax_received_account = cls.env.company.account_sale_tax_id.mapped(
            "invoice_repartition_line_ids.account_id"
        )

        def create_tax(percentage, price_include=False, include_base_amount=False):
            return cls.env["account.tax"].create(
                {
                    "name": f"Tax {percentage}%",
                    "amount": percentage,
                    "price_include": price_include,
                    "amount_type": "percent",
                    "include_base_amount": include_base_amount,
                    "invoice_repartition_line_ids": [
                        (
                            0,
                            0,
                            {
                                "repartition_type": "base",
                                "tag_ids": [Command.set(cls.tax_tag_invoice_base.ids)],
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "repartition_type": "tax",
                                "account_id": cls.tax_received_account.id,
                                "tag_ids": [Command.set(cls.tax_tag_invoice_tax.ids)],
                            },
                        ),
                    ],
                    "refund_repartition_line_ids": [
                        (
                            0,
                            0,
                            {
                                "repartition_type": "base",
                                "tag_ids": [Command.set(cls.tax_tag_refund_base.ids)],
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "repartition_type": "tax",
                                "account_id": cls.tax_received_account.id,
                                "tag_ids": [Command.set(cls.tax_tag_refund_tax.ids)],
                            },
                        ),
                    ],
                }
            )

        cls.tax7 = create_tax(7, price_include=False)

        wallet_product_template = cls.env["product.template"].create(
            {
                "name": "Wallet product with taxes",
                "type": "service",
                "is_customer_wallet_product": True,
                "property_account_expense_id": cls.customer_wallet_account.id,
                "property_account_income_id": cls.customer_wallet_account.id,
                "taxes_id": [Command.set(cls.tax7.ids)],
            }
        )
        cls.wallet_product.is_customer_wallet_product = False
        cls.wallet_product = wallet_product_template.product_variant_id

    def test_simple(self):
        """This tests a use-case that should never happen: the wallet product
        has taxes.
        """
        self.create_wallet_pos_payment(
            product=self.wallet_product,
            payment_method=self.cash_payment_method,
            amount=100,
        )
        self.assertEqual(self.partner.customer_wallet_balance, 100)

        self.pos_session.action_pos_session_close()
        self.assertEqual(self.partner.customer_wallet_balance, 100)

        wallet_move_line = self.env["account.move.line"].search(
            [
                ("partner_id", "=", self.partner.id),
                (
                    "account_id",
                    "=",
                    self.customer_wallet_account.id,
                ),
            ],
            limit=1,
        )
        self.assertEqual(wallet_move_line.credit, 100)
        move_id = wallet_move_line.move_id
        tax_line_id = move_id.line_ids.filtered(
            lambda line: line.account_id == self.tax_received_account
        )
        self.assertEqual(tax_line_id.credit, 7)
