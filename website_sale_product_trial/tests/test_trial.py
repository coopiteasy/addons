# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo.tests import common


class TestTrialContractBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_1 = cls.env.ref("product.product_product_1")
        cls.product_1.is_trial = True
        cls.product_2 = cls.env.ref("product.product_product_2")
        cls.product_2.is_trial = False
        cls.product_3 = cls.env.ref("product.product_product_3")
        cls.product_3.is_trial = True


class TestTrialContract(TestTrialContractBase):
    def test_is_product_compatible_empty(self):
        self.assertTrue(
            self.env["sale.order"]._is_product_compatible(
                self.env["product.product"],
            )
        )

    def test_is_product_compatible_mixed(self):
        self.assertFalse(
            self.env["sale.order"]._is_product_compatible(
                self.product_1 | self.product_2
            )
        )

    def test_is_product_compatible_only_trial(self):
        self.assertTrue(self.env["sale.order"]._is_product_compatible(self.product_1))
        self.assertFalse(
            self.env["sale.order"]._is_product_compatible(
                self.product_1 | self.product_3
            )
        )

    def test_is_product_compatible_only_non_trial(self):
        self.assertTrue(self.env["sale.order"]._is_product_compatible(self.product_2))
