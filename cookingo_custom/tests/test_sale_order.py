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

    def test_find_containers(self):
        """Find containers that will fit the required volumes."""
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
        volumes = self.sale_order.calculate_volume_containers()[self.salad_template]
        result_1 = self.sale_order.find_containers_for_volume(volumes[0])
        result_2 = self.sale_order.find_containers_for_volume(volumes[1])

        self.assertEqual(len(result_1), 1)
        self.assertEqual(result_1, [self.containers[1200].product_variant_id])
        self.assertEqual(len(result_2), 1)
        self.assertEqual(result_2, [self.containers[600].product_variant_id])

    def test_find_containers_container_is_zero(self):
        """When the value of container_2_volume is 0, don't add two containers."""
        self.salad_template.container_2_volume = 0
        order_line = self.env["sale.order.line"].create(
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
        volumes = self.sale_order.calculate_volume_containers()[self.salad_template]
        result_1 = self.sale_order.find_containers_for_volume(volumes[0])
        result_2 = self.sale_order.find_containers_for_volume(volumes[1])

        self.assertEqual(len(result_1), 1)
        self.assertEqual(len(result_2), 0)

    def test_add_containers(self):
        """When adding containers to a cart that contains a single item, expect
        two correctly sized containers."""
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        self.sale_order.add_containers()

        self.assertEqual(len(self.sale_order.order_line), 3)

        products = [line.product_id for line in self.sale_order.order_line]
        self.assertIn(self.salad_product_adult, products)
        self.assertIn(self.containers[600].product_variant_id, products)
        self.assertIn(self.containers[400].product_variant_id, products)

        lines = self.sale_order.order_line.filtered(
            lambda line: line.product_id.is_container
        )
        for line in lines:
            self.assertEqual(line.product_uom_qty, 1)

    def test_add_containers_twice(self):
        """When doing add_containers() twice, don't end up with four containers."""
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        self.sale_order.add_containers()
        self.sale_order.add_containers()

        self.assertEqual(len(self.sale_order.order_line), 3)
        lines = self.sale_order.order_line.filtered(
            lambda line: line.product_id.is_container
        )
        for line in lines:
            self.assertEqual(line.product_uom_qty, 1)

    def test_add_to_cart_twice(self):
        """When adding a single meal twice, don't end up with four containers."""
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        salad_line = self.sale_order.order_line[0]
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id,
            line_id=salad_line.id,
            add_qty=1,
            set_qty=0,
        )
        self.sale_order.add_containers()

        self.assertEqual(len(self.sale_order.order_line), 3)

        products = [line.product_id for line in self.sale_order.order_line]
        self.assertIn(self.salad_product_adult, products)
        self.assertIn(self.containers[1200].product_variant_id, products)
        self.assertIn(self.containers[600].product_variant_id, products)

        lines = self.sale_order.order_line.filtered(
            lambda line: line.product_id.is_container
        )
        for line in lines:
            self.assertEqual(line.product_uom_qty, 1)

    def test_remove_containers_after_adding_to_cart(self):
        """When a new item is added to the cart, remove all containers."""
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        salad_line = self.sale_order.order_line[0]
        self.sale_order.add_containers()
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id,
            line_id=salad_line.id,
            add_qty=1,
            set_qty=0,
        )

        self.assertEqual(len(self.sale_order.order_line), 1)
