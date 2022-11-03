# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError

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
        self.assertAlmostEqual(
            abs(deposit_line.price_total), self.partner.current_deposit
        )

        previous_deposit = self.partner.current_deposit
        container_lines = self.sale_order.order_line.filtered("product_id.is_container")
        container_price = sum(line.price_total for line in container_lines)
        self.sale_order.action_done()

        self.assertGreater(self.partner.current_deposit, previous_deposit)
        self.assertAlmostEqual(self.partner.current_deposit, container_price)

    def test_buy_less_expensive_meal(self):
        """When buying a less expensive meal than the previous one, give the
        entire deposit as discount. The deposit goes down in this way.
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
        other_lines = self.sale_order.order_line.filtered(
            lambda line: line != deposit_line
        )
        self.assertGreater(abs(deposit_line.price_total), container_price)
        self.assertAlmostEqual(
            self.sale_order.amount_total,
            sum(line.price_total for line in other_lines)
            - abs(deposit_line.price_total),
        )

        previous_deposit = self.partner.current_deposit
        self.sale_order.action_done()

        self.assertLess(self.partner.current_deposit, previous_deposit)
        self.assertAlmostEqual(
            self.partner.current_deposit
            + (abs(deposit_line.price_total) - container_price),
            previous_deposit,
        )

    def test_massive_deposit_small_order(self):
        """If a customer has a huge deposit, don't give a discount greater than
        the total price of the order.
        """
        big_sale_order = self.env["sale.order"].create(
            {
                "name": "Big Sale",
                "partner_id": self.partner.id,
                "partner_invoice_id": self.partner.id,
                "partner_shipping_id": self.partner.id,
                "pricelist_id": self.pricelist.id,
            }
        )
        big_sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=100, set_qty=0
        )
        big_sale_order.add_containers()
        big_sale_order.action_done()

        self.sale_order._cart_update(
            product_id=self.salad_product_adult.id, line_id=None, add_qty=1, set_qty=0
        )
        self.sale_order.add_containers()

        self.assertAlmostEqual(self.sale_order.amount_total, 0)

        deposit_line = self.sale_order.order_line.filtered(
            lambda line: line.product_id == self.container_deposit_product
        )
        other_lines = self.sale_order.order_line.filtered(
            lambda line: line != deposit_line
        )
        cum_price_other_lines = sum(line.price_total for line in other_lines)

        self.assertAlmostEqual(
            abs(deposit_line.price_total), abs(cum_price_other_lines)
        )

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

    def test_container_not_returned(self):
        """If a container was not returned, dock it from the customer's deposit."""
        previous_deposit = self.partner.current_deposit
        container_line = self.previous_sale_order.order_line.filtered(
            lambda line: line.product_id == self.containers[400].product_variant_id
        )
        container_line.not_returned = 1

        self.assertLess(self.partner.current_deposit, previous_deposit)

    def test_container_not_returned_invalid_values(self):
        """Test the constraints of not_returned."""
        container_line = self.previous_sale_order.order_line.filtered(
            lambda line: line.product_id == self.containers[400].product_variant_id
        )
        meal_line = self.previous_sale_order.order_line.filtered("product_id.is_meal")

        with self.assertRaises(ValidationError):
            container_line.not_returned = -1
        with self.assertRaises(ValidationError):
            container_line.not_returned = 2
        with self.assertRaises(ValidationError):
            meal_line.not_returned = 1
