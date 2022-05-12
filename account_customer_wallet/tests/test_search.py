# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestBalance


class TestSearch(TestBalance):
    def test_search_balance_all_zero(self):
        """On a virgin database, all balances are zero."""
        all_partners = self.env["res.partner"].search([])

        for domain in (
            [("customer_wallet_balance", "=", 0)],
            [("customer_wallet_balance", "!=", 1)],
            [("customer_wallet_balance", ">", -1)],
            [("customer_wallet_balance", ">=", -1)],
            [("customer_wallet_balance", ">=", 0)],
            [("customer_wallet_balance", "<", 1)],
            [("customer_wallet_balance", "<=", 1)],
            [("customer_wallet_balance", "<=", 0)],
            [("customer_wallet_balance", "=?", 0)],
            [("customer_wallet_balance", "in", [0])],
            [("customer_wallet_balance", "not in", [1, -1])],
        ):
            self.assertEqual(self.env["res.partner"].search(domain), all_partners)

    def test_search_balance_positive(self):
        """Adjust the balance of one partner, and search it. Make sure that
        other partners are not matched by the search.
        """
        self._create_move(credit=100)
        for domain in (
            [("customer_wallet_balance", "=", 100)],
            [("customer_wallet_balance", "!=", 0)],
            [("customer_wallet_balance", ">", 50)],
            [("customer_wallet_balance", ">=", 50)],
            [("customer_wallet_balance", ">=", 100)],
            [("customer_wallet_balance", "=?", 100)],
            [("customer_wallet_balance", "in", [100])],
            [("customer_wallet_balance", "not in", [0])],
        ):
            result = self.env["res.partner"].search(domain)
            self.assertTrue(self.partner in result)
            self.assertFalse(self.env.ref("base.res_partner_address_31") in result)
            # partner and parent
            self.assertEqual(len(result), 2)

    def test_search_balance_negative(self):
        """Same as test_search_balance_positive, but for the lesser-than operators."""
        self._create_move(debit=100)
        for domain in (
            [("customer_wallet_balance", "<", -50)],
            [("customer_wallet_balance", "<=", -50)],
            [("customer_wallet_balance", "<=", -100)],
        ):
            result = self.env["res.partner"].search(domain)
            self.assertTrue(self.partner in result)
            self.assertFalse(self.env.ref("base.res_partner_address_31") in result)
            # partner and parent
            self.assertEqual(len(result), 2)

    def test_search_balance_not_implemented(self):
        """like and ilike are not implemented."""
        self._create_move(credit=100)
        for domain in (
            [("customer_wallet_balance", "=like", None)],
            [("customer_wallet_balance", "like", None)],
            [("customer_wallet_balance", "not like", None)],
            [("customer_wallet_balance", "ilike", None)],
            [("customer_wallet_balance", "not ilike", None)],
            [("customer_wallet_balance", "=ilike", None)],
        ):
            with self.assertRaises(NotImplementedError):
                self.env["res.partner"].search(domain)
