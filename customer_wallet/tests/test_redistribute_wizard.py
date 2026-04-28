# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.exceptions import UserError

from .common import TestCommon


class TestRedistributeWizard(TestCommon):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        cls.RedistributeWizard = cls.env["customer.wallet.redistribute.wizard"]
        cls.RedistributeWizardLine = cls.env["customer.wallet.redistribute.wizard.line"]
        cls.other_partner_1 = cls.env["res.partner"].create(
            {
                "name": "Other Partner 1",
                "company_id": cls.partner.company_id.id,
            }
        )
        cls.other_partner_2 = cls.env["res.partner"].create(
            {
                "name": "Other Partner 2",
                "company_id": cls.partner.company_id.id,
            }
        )

    def _redistribute(self, amount, redistribution_configuration):
        wizard = self.RedistributeWizard.create({"partner_id": self.partner.id})
        for line in redistribution_configuration:
            self.RedistributeWizardLine.create(
                {"wizard_id": wizard.id, "partner_id": line[0].id, "amount": line[1]}
            )
        wizard.button_redistribute()

    def test_redistribution_wizard_no_transfer(self):
        with self.assertRaises(UserError):
            self._redistribute(0.0, [])

        with self.assertRaises(UserError):
            self._redistribute(999.0, [])

    def test_redistribution_wizard_one_transfer(self):
        self._create_move(credit=100)

        self.assertEqual(self.partner.customer_wallet_balance, 100)
        self.assertEqual(self.other_partner_1.customer_wallet_balance, 0)

        self._redistribute(30.0, [(self.other_partner_1, 30)])

        self.assertEqual(self.partner.customer_wallet_balance, 70)
        self.assertEqual(self.other_partner_1.customer_wallet_balance, 30)

    def test_redistribution_wizard_many_transfer(self):
        self._create_move(credit=1000)

        self.assertEqual(self.partner.customer_wallet_balance, 1000)
        self.assertEqual(self.other_partner_1.customer_wallet_balance, 0)
        self.assertEqual(self.other_partner_2.customer_wallet_balance, 0)

        self._redistribute(
            600.0, [(self.other_partner_1, 250), (self.other_partner_2, 350)]
        )

        self.assertEqual(self.partner.customer_wallet_balance, 400)
        self.assertEqual(self.other_partner_1.customer_wallet_balance, 250)
        self.assertEqual(self.other_partner_2.customer_wallet_balance, 350)
