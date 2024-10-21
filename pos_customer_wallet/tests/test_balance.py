# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


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
