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
