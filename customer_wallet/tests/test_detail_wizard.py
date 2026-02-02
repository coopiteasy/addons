# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from .common import TestCommon


class TestDetailWizard(TestCommon):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        cls.DetailWizard = cls.env["customer.wallet.detail.wizard"]

    def _get_wizard(self):
        return self.DetailWizard.create({"partner_id": self.partner.id})

    def test_detail_wizard_no_move(self):
        wizard = self._get_wizard()
        self.assertEqual(wizard.customer_wallet_balance, 0.0)
        self.assertNotIn("<tbody>", wizard.detail)

    def test_detail_wizard_one_move(self):
        self._create_move(credit=10)

        wizard = self._get_wizard()
        self.assertEqual(wizard.customer_wallet_balance, 10.0)
        self.assertIn("<tbody>", wizard.detail)
        self.assertIn("10.0", wizard.detail)

    def test_detail_wizard_many_moves(self):
        self._create_move(credit=10)
        self._create_move(credit=20)

        wizard = self._get_wizard()
        self.assertEqual(wizard.customer_wallet_balance, 30.0)
        self.assertIn("<tbody>", wizard.detail)
        self.assertIn("10.0", wizard.detail)
        self.assertIn("20.0", wizard.detail)
        self.assertIn("30.0", wizard.detail)
