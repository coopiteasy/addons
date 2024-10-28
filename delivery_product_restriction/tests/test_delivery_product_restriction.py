# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common


class TestDeliveryProductRestriction(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.SaleOrder = cls.env["sale.order"]
        cls.SaleOrderLine = cls.env["sale.order.line"]
        cls.DeliveryCarrier = cls.env["delivery.carrier"]

        cls.partner_18 = cls.env.ref("base.res_partner_18")
        cls.pricelist = cls.env.ref("product.list0")
        cls.product_6 = cls.env.ref("product.product_product_6")
        cls.product_8 = cls.env.ref("product.product_product_8")
        cls.product_uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product_delivery = cls.env.ref("delivery.product_product_delivery_normal")
        # Create delivery carrier
        cls.free_delivery = cls.DeliveryCarrier.create(
            {
                "name": "Free Delivery",
                "fixed_price": 0.0,
                "sequence": 1,
                "delivery_type": "fixed",
                "product_id": cls.product_delivery.id,
            }
        )
        cls.pick_delivery = cls.DeliveryCarrier.create(
            {
                "name": "Pick Delivery",
                "fixed_price": 0.0,
                "sequence": 1,
                "delivery_type": "fixed",
                "product_id": cls.product_delivery.id,
            }
        )
        cls.fixed_delivery = cls.DeliveryCarrier.create(
            {
                "name": "Fixed Price Delivery",
                "fixed_price": 10.0,
                "sequence": 1,
                "delivery_type": "fixed",
                "product_id": cls.product_delivery.id,
            }
        )

    def test_no_restriction(self):
        # Create order that don't match the delivery rules
        sale_order = self.SaleOrder.create(
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

        delivery_wizard = Form(
            self.env["choose.delivery.carrier"].with_context(
                default_order_id=sale_order.id
            )
        )

        self.assertTrue(self.free_delivery in delivery_wizard.available_carrier_ids)
        self.assertTrue(self.pick_delivery in delivery_wizard.available_carrier_ids)
        self.assertTrue(self.fixed_delivery in delivery_wizard.available_carrier_ids)

    def test_restricted(self):
        # Create restriction on delivery carrier for product_8
        self.product_8.restrict_delivery_carrier_to = self.pick_delivery
        # Create order that matches the delivery rules
        sale_order = self.SaleOrder.create(
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

        delivery_wizard = Form(
            self.env["choose.delivery.carrier"].with_context(
                default_order_id=sale_order.id
            )
        )

        self.assertTrue(self.free_delivery not in delivery_wizard.available_carrier_ids)
        self.assertTrue(self.pick_delivery in delivery_wizard.available_carrier_ids)
        self.assertTrue(
            self.fixed_delivery not in delivery_wizard.available_carrier_ids
        )
