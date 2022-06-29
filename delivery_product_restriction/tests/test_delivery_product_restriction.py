# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestDeliveryProductRestriction(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.SaleOrder = self.env["sale.order"]
        self.SaleOrderLine = self.env["sale.order.line"]
        self.DeliveryCarrier = self.env["delivery.carrier"]

        self.partner_18 = self.env.ref("base.res_partner_18")
        self.pricelist = self.env.ref("product.list0")
        self.product_6 = self.env.ref("product.product_product_6")
        self.product_8 = self.env.ref("product.product_product_8")
        self.product_uom_unit = self.env.ref("uom.product_uom_unit")
        self.product_delivery = self.env.ref("delivery.product_product_delivery_normal")
        # Create delivery carrier
        self.free_delivery = self.DeliveryCarrier.create(
            {
                "name": "Free Delivery",
                "fixed_price": 0.0,
                "sequence": 1,
                "delivery_type": "fixed",
                "product_id": self.product_delivery.id,
            }
        )
        self.pick_delivery = self.DeliveryCarrier.create(
            {
                "name": "Pick Delivery",
                "fixed_price": 0.0,
                "sequence": 1,
                "delivery_type": "fixed",
                "product_id": self.product_delivery.id,
            }
        )
        self.fixed_delivery = self.DeliveryCarrier.create(
            {
                "name": "Fixed Price Delivery",
                "fixed_price": 10.0,
                "sequence": 1,
                "delivery_type": "fixed",
                "product_id": self.product_delivery.id,
            }
        )

    def test_no_restriction(self):
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
            }
        )

        self.assertTrue(self.free_delivery in self.sale_1.available_carrier_ids)
        self.assertTrue(self.pick_delivery in self.sale_1.available_carrier_ids)
        self.assertTrue(self.fixed_delivery in self.sale_1.available_carrier_ids)

    def test_restricted(self):
        # Create restriction on delivery carrier for product_8
        self.product_8.restrict_delivery_carrier_to = self.pick_delivery
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
            }
        )

        self.assertTrue(self.free_delivery not in self.sale_2.available_carrier_ids)
        self.assertTrue(self.pick_delivery in self.sale_2.available_carrier_ids)
        self.assertTrue(self.fixed_delivery not in self.sale_2.available_carrier_ids)
