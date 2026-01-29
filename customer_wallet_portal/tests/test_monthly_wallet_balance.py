# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from .common import TestCommon


class TestMonthlyBalance(TestCommon):
    def test_credit_is_not_counted(self):
        """credit = increasing customer wallet budget. Not counted."""
        self._create_move(credit=100)
        self.assertFalse(self.partner_id.customer_wallet_payments_per_month())

    def test_one_payment(self):
        """Simple case."""
        self._create_move(debit=10, date=datetime.date(2023, 1, 1))
        result = self.partner_id.customer_wallet_payments_per_month()
        self.assertEqual(result[(2023, 1)], 10)

    def test_two_payments(self):
        """More complex case."""
        self._create_move(debit=10, date=datetime.date(2023, 1, 1))
        self._create_move(debit=5, date=datetime.date(2023, 1, 31))
        result = self.partner_id.customer_wallet_payments_per_month()
        self.assertEqual(result[(2023, 1)], 15)

    def test_multiple_months(self):
        """Separate months have separate keys."""
        self._create_move(debit=10, date=datetime.date(2023, 1, 1))
        self._create_move(debit=20, date=datetime.date(2023, 2, 1))
        result = self.partner_id.customer_wallet_payments_per_month()
        self.assertEqual(result[(2023, 1)], 10)
        self.assertEqual(result[(2023, 2)], 20)
        self.assertEqual(len(result), 2)

    def test_multiple_years(self):
        """Identical months in different years have separate keys."""
        self._create_move(debit=10, date=datetime.date(2023, 1, 1))
        self._create_move(debit=20, date=datetime.date(2024, 1, 1))
        result = self.partner_id.customer_wallet_payments_per_month()
        self.assertEqual(result[(2023, 1)], 10)
        self.assertEqual(result[(2024, 1)], 20)
