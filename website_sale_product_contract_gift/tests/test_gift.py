# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import Command, fields
from odoo.tests import common


class TestGiftContractBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.today = fields.Date.today()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "partner test contract",
                "email": "demo@test.com",
            }
        )
        cls.partner_gift_to = cls.env["res.partner"].create(
            {
                "name": "partner gift to",
                "email": "partner_gift_to@test.com",
                "type": "delivery",
            }
        )
        cls.product_1 = cls.env.ref("product.product_product_1")
        cls.product_1.is_gift = True
        cls.product_2 = cls.env.ref("product.product_product_2")
        cls.product_2.is_gift = False


class TestGiftContract(TestGiftContractBase):
    def _get_gift_sale_order(self):
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "partner_shipping_id": self.partner_gift_to.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "date_start": self.today,
                        }
                    ),
                ],
            }
        )
        return order

    def _generate_contract_from_order(self):
        order = self._get_gift_sale_order()
        order.action_confirm()
        contract = order.order_line.gift_contract_id[0]
        return contract

    def test_check_gift_contract_date(self):
        contract = self._generate_contract_from_order()
        self.assertEqual(contract.date_start, self.today)
        self.assertEqual(contract.recurring_rule_type, "yearly")
        self.assertEqual(contract.recurring_interval, 1)
        for line in contract.contract_line_ids:
            self.assertEqual(line.recurring_rule_type, "yearly")
            self.assertEqual(line.recurring_interval, 1)

    def test_gift_contract_partner_with_existing_partner(self):
        existing_partner = self.env["res.partner"].create(
            {
                "name": "partner gift to existing partner",
                "email": "partner_gift_to@test.com",
                "type": "contact",
            }
        )
        contract = self._generate_contract_from_order()
        assert contract.partner_id.id != self.partner_gift_to.id
        assert contract.partner_id.id == existing_partner.id
        assert self.partner_gift_to.parent_id == existing_partner
        assert contract.partner_id.type == "contact"

    def test_gift_contract_partner_without_existing_partner(self):
        contract = self._generate_contract_from_order()
        assert contract.partner_id.id == self.partner_gift_to.id
        self.assertFalse(self.partner_gift_to.parent_id.id)
        assert contract.partner_id.type == "contact"

    def test_gift_contract_is_gift(self):
        contract = self._generate_contract_from_order()
        self.assertTrue(contract.is_gift)

    def test_gift_contract_invoice_generation(self):
        contract = self._generate_contract_from_order()
        contract.cron_recurring_create_invoice(date_ref=self.today)
        invoices = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("partner_id", "=", contract.partner_id.id),
            ]
        )
        self.assertEqual(len(invoices), 1)
        self.assertTrue(
            any(invoices.line_ids.contract_line_id.contract_id.mapped("is_gift"))
        )

    def test_gift_contract_user_creation(self):
        contract = self._generate_contract_from_order()
        self.assertFalse(contract.partner_id.user_id)
        contract.cron_recurring_create_invoice(date_ref=self.today)
        self.assertTrue(contract.partner_id.user_ids)

    def test_find_contact_partners(self):
        """Test method `find_contact_partners()`."""
        # existing partners
        partner1 = self.env["res.partner"].create(
            {
                "name": "Test1 Test",
                "email": "test@test.tld",
                "type": "contact",
                "country_id": 1,
                "zip": 1000,
            }
        )
        partner2 = self.env["res.partner"].create(
            {
                "name": "Test2 Test",
                "email": "test@test.tld",
                "type": "contact",
                "country_id": 1,
                "zip": 1000,
            }
        )
        # new partner with a match
        partner_new = self.env["res.partner"].new(
            {
                "name": "Test2 Test",
                "email": "test@test.tld",
                "type": "contact",
                "country_id": 1,
                "zip": 1000,
            }
        )
        self.assertEqual(
            self.env["sale.order"].find_contact_partners(partner_new),
            partner2,
        )
        # new partner without a match
        partner_new = self.env["res.partner"].new(
            {
                "name": "Test Test",
                "email": "test@test.tld",
                "type": "contact",
                "country_id": 1,
                "zip": 2000,
            }
        )
        self.assertEqual(
            self.env["sale.order"].find_contact_partners(partner_new),
            partner1 | partner2,
        )

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

    def test_is_product_compatible_only_gift(self):
        self.assertTrue(self.env["sale.order"]._is_product_compatible(self.product_1))

    def test_is_product_compatible_only_non_gift(self):
        self.assertTrue(self.env["sale.order"]._is_product_compatible(self.product_2))
