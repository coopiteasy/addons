# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import TransactionCase


class TestProductProduct(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_unit_price_margin_classification = cls.env[
            "product.margin.classification"
        ].create(
            {
                "markup": 28,
                "name": "unit price test margin",
                "price_round": 0.01,
                "price_surcharge": 0,
            }
        )

        cls.test_unit_price_product = cls.env["product.product"].create(
            {
                "name": "test product",
                "standard_price": 23.76,
                "uom_id": cls.env.ref("uom.product_uom_dozen").id,
                "list_price": 15,
                "margin_classification_id": cls.test_unit_price_margin_classification.id,
            }
        )

    def test_price_computation(self):
        self.test_unit_price_product._compute_theoretical_multi()
        self.assertEqual(self.test_unit_price_product.theoretical_price, 30.36)
