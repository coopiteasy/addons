# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import common


class TestSaleOrder(common.TestCommon):
    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)

        self.pricelist = self.env["product.pricelist"].create(
            {"name": "Default Pricelist"}
        )

        self.sale_order = self.env["sale.order"].create(
            {
                "name": "Sale",
                "partner_id": self.env.ref("base.user_admin").id,
                "partner_invoice_id": self.env.ref("base.user_admin").id,
                "partner_shipping_id": self.env.ref("base.user_admin").id,
                "pricelist_id": self.pricelist.id,
            }
        )

        return result

    def test_double_volume_two_meals(self):
        """When two meals are added, the required volume doubles."""
        order_line = self.env["sale.order.line"].create(
            {
                "name": self.salad_product_adult.name,
                "product_id": self.salad_product_adult.id,
                "product_uom_qty": 2,
                "product_uom": self.salad_product_adult.uom_id.id,
                "price_unit": self.salad_product_adult.list_price,
                "order_id": self.sale_order.id,
                "tax_id": False,
            }
        )
        result = self.sale_order.calculate_volume_containers()

        # One product template.
        self.assertEqual(len(result), 1)

        container_volumes = result[self.salad_template]
        self.assertEqual(
            container_volumes[0], self.salad_product_adult.container_1_volume * 2
        )
        self.assertEqual(
            container_volumes[1], self.salad_product_adult.container_2_volume * 2
        )

    def test_adult_and_child_portion(self):
        """When an adult and child portion are added, the required volume
        (almost) doubles.
        """
        order_line_adult = self.env["sale.order.line"].create(
            {
                "name": self.salad_product_adult.name,
                "product_id": self.salad_product_adult.id,
                "product_uom_qty": 1,
                "product_uom": self.salad_product_adult.uom_id.id,
                "price_unit": self.salad_product_adult.list_price,
                "order_id": self.sale_order.id,
                "tax_id": False,
            }
        )
        order_line_child = self.env["sale.order.line"].create(
            {
                "name": self.salad_product_child.name,
                "product_id": self.salad_product_child.id,
                "product_uom_qty": 1,
                "product_uom": self.salad_product_child.uom_id.id,
                "price_unit": self.salad_product_child.list_price,
                "order_id": self.sale_order.id,
                "tax_id": False,
            }
        )

        result = self.sale_order.calculate_volume_containers()

        # One product template.
        self.assertEqual(len(result), 1)

        container_volumes = result[self.salad_template]
        self.assertEqual(
            container_volumes[0],
            self.salad_product_adult.container_1_volume
            + self.salad_product_child.container_1_volume,
        )
        self.assertEqual(
            container_volumes[1],
            self.salad_product_adult.container_2_volume
            + self.salad_product_child.container_2_volume,
        )

    def test_not_a_meal(self):
        """When the order doesn't contain meals, don't calculate
        volumes.
        """
        desk = self.env.ref("product.product_product_4")
        order_line = self.env["sale.order.line"].create(
            {
                "name": desk.name,
                "product_id": desk.id,
                "product_uom_qty": 2,
                "product_uom": desk.uom_id.id,
                "price_unit": desk.list_price,
                "order_id": self.sale_order.id,
                "tax_id": False,
            }
        )

        result = self.sale_order.calculate_volume_containers()

        self.assertFalse(result)
