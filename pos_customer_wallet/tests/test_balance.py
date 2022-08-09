# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields

from .common import TestPosBalance as TestBalance


class TestPosBalance(TestBalance):
    def test_with_statement(self):
        """Bank statements now also affect balance."""
        self._create_move(credit=100)
        self._create_statement(amount=40)

        self.assertEqual(self.partner.customer_wallet_balance, 60)

    def test_statement_different_partner(self):
        """Statements for other partners do not affect the balances of all
        clients.
        """
        other_partner = self.env.ref("base.res_partner_address_31")
        self._create_statement(amount=100, partner=other_partner)

        self.assertEqual(self.partner.customer_wallet_balance, 0)
        self.assertEqual(other_partner.customer_wallet_balance, -100)

    def test_credit_by_product(self):
        # Intialize wallet with 500
        self._create_move(credit=500)

        self.pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "currency_id": self.env.user.company_id.currency_id.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "list_price",
                        },
                    )
                ],
            }
        )

        self.wallet_product = self.env.ref(
            "account_customer_wallet.product_wallet_demo"
        )

        # Create a new pos config and open it
        self.pos_config = self.env.ref("point_of_sale.pos_config_main").copy(
            {
                "available_pricelist_ids": [(6, 0, self.pricelist.ids)],
                "pricelist_id": self.pricelist.id,
            }
        )
        self.pos_config.open_session_cb()

        self.cash_journal = self.pos_config.journal_ids.filtered(
            lambda x: x.type == "cash"
        )
        self.cash_statement = self.pos_config.current_session_id.statement_ids.filtered(
            lambda x: x.journal_id.type == "cash"
        )
        self.receivable_account = (
            self.env.user.partner_id.property_account_receivable_id
        )

        # Make an order
        order_data = {
            "id": u"0006-001-0010",
            "to_invoice": False,
            "data": {
                "creation_date": u"2022-01-01 12:00:00",
                "name": "Order 0006-001-0010",
                "uid": u"00001-001-0001",
                "pricelist_id": self.pricelist.id,
                "user_id": self.env.user.id,
                "partner_id": self.partner.id,
                "fiscal_position_id": False,
                "sequence_number": 1,
                "amount_tax": 0,
                "amount_return": 0,
                "amount_total": 1000.0,
                "amount_paid": 1000,
                "pos_session_id": self.pos_config.current_session_id.id,
                "lines": [
                    [
                        0,
                        0,
                        {
                            "product_id": self.wallet_product.id,
                            "price_unit": 1,
                            "qty": 1000,
                            "price_subtotal": 1000.0,
                            "price_subtotal_incl": 1000.0,
                            "tax_ids": False,
                        },
                    ]
                ],
                "statement_ids": [
                    [
                        0,
                        0,
                        {
                            "journal_id": self.cash_journal.id,
                            "amount": 1000.0,
                            "name": fields.Datetime.now(),
                            "account_id": self.receivable_account.id,
                            "statement_id": self.cash_statement.id,
                        },
                    ]
                ],
            },
        }

        # Buy 1000 of wallet product
        self.env["pos.order"].create_from_ui([order_data])

        self.assertEqual(self.partner.customer_wallet_balance, 1500)
