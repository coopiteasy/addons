# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import common


class TestDeposit(common.TestCommonDeposit):
    def test_buy_same_meal(self):
        """When buying an identical meal as the previous one, the deposit covers
        the combined price of the containers.
        """
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        self.sale_order.add_containers()

        # Meal, two containers, deposit
        self.assertEqual(len(self.sale_order.order_line), 4)
        deposit_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == self.container_deposit_product
        )
        self.assertAlmostEqual(deposit_line.price_total, -self.partner.current_deposit)

    def test_buy_more_expensive_meal(self):
        """When buying a more expensive meal than the previous one, the deposit
        only covers as much as the previous meal, and is then raised afterwards.
        """
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=4, set_qty=0
        )
        self.sale_order.add_containers()

        # Meal, two containers, deposit
        self.assertEqual(len(self.sale_order.order_line), 4)
        deposit_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == self.container_deposit_product
        )
        self.assertAlmostEqual(deposit_line.price_total, -self.partner.current_deposit)

        previous_deposit = self.partner.current_deposit
        container_lines = self.sale_order.order_line.filtered("product_id.is_container")
        container_price = sum(line.price_total for line in container_lines)
        self.sale_order.action_done()

        self.assertGreater(self.partner.current_deposit, previous_deposit)
        self.assertAlmostEqual(self.partner.current_deposit, container_price)

    def test_buy_less_expensive_meal(self):
        """When buying a less expensive meal than the previous one---even though
        the deposit could cover a greater amount---don't cover that much.
        """
        self.salad_template.container_2_volume = 0
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        self.sale_order.add_containers()

        # Meal, one container, deposit
        self.assertEqual(len(self.sale_order.order_line), 3)
        deposit_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == self.container_deposit_product
        )
        container_lines = self.sale_order.order_line.filtered("product_id.is_container")
        container_price = sum(line.price_total for line in container_lines)
        self.assertGreater(deposit_line.price_total, -self.partner.current_deposit)
        self.assertAlmostEqual(deposit_line.price_total, -container_price)

        previous_deposit = self.partner.current_deposit
        self.sale_order.action_done()

        self.assertAlmostEqual(self.partner.current_deposit, previous_deposit)

    def test_no_deposit_yet(self):
        """If the customer has no deposit yet, don't add a deposit line to the
        sale order.
        """
        self.previous_sale_order.action_cancel()
        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        self.sale_order.add_containers()

        # Meal, two containers
        self.assertEqual(len(self.sale_order.order_line), 3)
        deposit_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == self.container_deposit_product
        )
        self.assertFalse(deposit_line)
