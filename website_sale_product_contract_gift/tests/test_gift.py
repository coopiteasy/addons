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
                "email": "demo@demo.com",
            }
        )
        cls.partner_gift_to = cls.env["res.partner"].create(
            {
                "name": "partner gift to",
                "email": "partner_gift_to@demo.com",
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

    def _get_contract_from_order(self):
        order = self._get_gift_sale_order()
        order.action_confirm()
        contract = order.order_line.mapped("gift_contract_id")[0]
        return contract

    def test_check_gift_contract_date(self):
        contract = self._get_contract_from_order()
        assert contract.date_start == self.today

    def test_gift_contract_partner(self):
        contract = self._get_contract_from_order()
        assert contract.partner_id.id != self.partner_gift_to.id
        assert contract.partner_id.name == self.partner_gift_to.name
        assert contract.partner_id.email == self.partner_gift_to.email
        assert contract.partner_id.street == self.partner_gift_to.street
        assert contract.partner_id.type == "contact"

    def test_gift_contract_is_gift(self):
        contract = self._get_contract_from_order()
        self.assertTrue(contract.is_gift)

    def test_gift_contract_invoice_generation(self):
        contract = self._get_contract_from_order()
        contract.cron_recurring_create_invoice(date_ref=self.today)
        invoices = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("partner_id", "=", contract.partner_id.id),
            ]
        )
        self.assertEqual(len(invoices), 1)
        self.assertTrue(
            any(
                invoices.mapped("line_ids")
                .mapped("contract_line_id")
                .mapped("contract_id")
                .mapped("is_gift")
            )
        )

    def test_gift_contract_user_creation(self):
        contract = self._get_contract_from_order()
        self.assertFalse(contract.partner_id.user_id)
        contract.cron_recurring_create_invoice(date_ref=self.today)
        self.assertTrue(contract.partner_id.user_ids)
