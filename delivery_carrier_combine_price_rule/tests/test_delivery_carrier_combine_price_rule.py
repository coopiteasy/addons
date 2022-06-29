# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import common


class TestDeliveryCombinePriceRule(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.SaleOrder = self.env["sale.order"]
        self.SaleOrderLine = self.env["sale.order.line"]

        self.partner_18 = self.env.ref("base.res_partner_18")
        self.pricelist = self.env.ref("product.list0")
        self.product_6 = self.env.ref("product.product_product_6")
        self.product_8 = self.env.ref("product.product_product_8")
        self.product_uom_unit = self.env.ref("uom.product_uom_unit")
        self.delivery_carrier = self.env.ref(
            "delivery_carrier_combine_price_rule.delivery_carrier"
        )

    def test_combined_price_rule_no_match(self):
        # Create order that don't match the delivery rules
        self.sale_1 = self.SaleOrder.create(
            {
                "partner_id": self.partner_18.id,
                "partner_invoice_id": self.partner_18.id,
                "partner_shipping_id": self.partner_18.id,
                "pricelist_id": self.pricelist.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product_6.name,
                            "product_id": self.product_6.id,
                            "product_uom_qty": 1,
                            "product_uom": self.product_uom_unit.id,
                            "price_unit": self.product_6.list_price,
                        },
                    )
                ],
                "carrier_id": self.delivery_carrier.id,
            }
        )

        # Raise exception because price is less than 1000
        with self.assertRaises(UserError):
            self.delivery_carrier._get_price_available(self.sale_1)

    def test_combined_price_rule_ok(self):
        # Create order that matches the delivery rules
        self.sale_2 = self.SaleOrder.create(
            {
                "partner_id": self.partner_18.id,
                "partner_invoice_id": self.partner_18.id,
                "partner_shipping_id": self.partner_18.id,
                "pricelist_id": self.pricelist.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product_6.name,
                            "product_id": self.product_6.id,
                            "product_uom_qty": 1,
                            "product_uom": self.product_uom_unit.id,
                            "price_unit": self.product_6.list_price,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": self.product_8.name,
                            "product_id": self.product_8.id,
                            "product_uom_qty": 1,
                            "product_uom": self.product_uom_unit.id,
                            "price_unit": self.product_8.list_price,
                        },
                    ),
                ],
                "carrier_id": self.delivery_carrier.id,
            }
        )

        # Should not raise exception as all rules are true for this sale
        price = self.delivery_carrier._get_price_available(self.sale_2)
        self.assertEqual(price, 20 + 10, "Price of the delivery not correct")
