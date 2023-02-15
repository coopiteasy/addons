# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timedelta
from itertools import combinations

from odoo.tests.common import Form, SavepointCase


class TestResourceBooking(SavepointCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)

        cls.partner_id = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.product_template_id = cls.env["product.template"].create(
            {
                "name": "Test Product",
            }
        )
        cls.product_id = cls.product_template_id.product_variant_id
        cls.calendar_id = cls.env["resource.calendar"].create(
            {
                "name": "Test Calendar",
                "attendance_ids": [
                    (
                        0,
                        False,
                        {
                            "name": "Test Day",
                            "dayofweek": "0",  # Monday
                            "hour_from": 0,
                            "hour_to": 23.99,
                        },
                    )
                ],
            }
        )
        cls.resource_product_template_id = cls.env["product.template"].create(
            {
                "name": "Test Resource Product",
            }
        )
        cls.resource_product_id = cls.resource_product_template_id.product_variant_id
        cls.resource_id = cls.env["resource.resource"].create(
            {
                "name": "Test Resource",
                "resource_type": "material",
                "product_id": cls.resource_product_id.id,
            }
        )
        cls.combination_id = cls.env["resource.booking.combination"].create(
            {
                "resource_ids": [cls.resource_id.id],
            }
        )
        cls.booking_type_id = cls.env["resource.booking.type"].create(
            {
                "name": "Test Booking Type",
                "duration": 1,
                "resource_calendar_id": cls.calendar_id.id,
                "default_product_id": cls.product_id.id,
            }
        )
        cls.env["resource.booking.type.combination.rel"].create(
            {
                "combination_id": cls.combination_id.id,
                "type_id": cls.booking_type_id.id,
            }
        )

        # Also create a booking type with many resources/combinations
        cls.many_resources = cls.env["resource.resource"]
        for i in range(4):
            template_id = cls.env["product.template"].create(
                {
                    "name": "Test Resource Product",
                }
            )
            product_id = template_id.product_variant_id
            cls.many_resources += cls.env["resource.resource"].create(
                {
                    "name": f"Test Resource {i}",
                    "resource_type": "material",
                    "product_id": product_id.id,
                }
            )
        cls.many_combinations = cls.env["resource.booking.combination"].union(
            *[
                cls.env["resource.booking.combination"].create(
                    {"resource_ids": [combination[0].id, combination[1].id]}
                )
                for combination in combinations(cls.many_resources, 2)
            ]
        )
        cls.many_booking_type_id = cls.env["resource.booking.type"].create(
            {
                "name": "Test Booking Type Many Combinations",
                "duration": 1,
                "resource_calendar_id": cls.calendar_id.id,
                "default_product_id": cls.product_id.id,
            }
        )
        for combination_id in cls.many_combinations:
            cls.env["resource.booking.type.combination.rel"].create(
                {
                    "combination_id": combination_id.id,
                    "type_id": cls.many_booking_type_id.id,
                }
            )

        # Grab the next Monday. We can book resources on that day.
        target_date = datetime.now() + timedelta(days=1)
        while target_date.weekday() != 0:
            target_date += timedelta(days=1)
        cls.target_date = target_date.replace(hour=9, minute=0, second=0)

    def create_booking(
        self,
        partner_id=None,
        booking_type_id=None,
        product_id=None,
        target_date=None,
        duration=None,
        combination_id=None,
    ):
        return self.env["resource.booking"].create(
            {
                "partner_id": partner_id
                if partner_id is not None
                else self.partner_id.id,
                "type_id": booking_type_id
                if booking_type_id is not None
                else self.booking_type_id.id,
                "product_id": product_id
                if product_id is not None
                else self.product_id.id,
                "start": target_date if target_date is not None else self.target_date,
                "duration": duration if duration is not None else 1,
                "combination_id": combination_id
                if combination_id is not None
                else self.combination_id.id,
                "combination_auto_assign": False,
            }
        )

    def test_create_sale_order(self):
        """When creating a resource.booking, also create and link a sale order."""
        booking_id = self.create_booking()
        self.assertTrue(booking_id.sale_order_id)
        self.assertEqual(booking_id.sale_order_line_ids[0].product_id, self.product_id)
        self.assertEqual(
            booking_id.sale_order_line_ids[1].product_id, self.resource_product_id
        )

    def test_create_sale_order_no_product(self):
        """When creating a resource booking without a product, don't include a
        sale order line for the non-existent product.
        """
        self.resource_id.product_id = False
        booking_id = self.create_booking(product_id=False)
        self.assertEqual(len(booking_id.sale_order_line_ids), 0)

    def test_default_product_id(self):
        """When a product is defined on the type, use that as default."""
        with Form(self.env["resource.booking"]) as form:
            form.partner_id = self.partner_id
            self.assertFalse(form.product_id)
            form.type_id = self.booking_type_id
            self.assertEqual(form.product_id, self.product_id)

    def test_cancel_booking_cancels_sale_order(self):
        """When cancelling a booking, cancel its sale order."""
        booking_id = self.create_booking()
        booking_id.action_cancel()
        self.assertEqual(booking_id.sale_order_id.state, "cancel")

    def test_sale_order_confirm(self):
        booking_id = self.create_booking()
        booking_id.action_sale_order_confirm()
        self.assertEqual(booking_id.sale_order_id.state, "sale")

    def test_sale_order_quotation_send(self):
        booking_id = self.create_booking()
        result = booking_id.action_sale_order_quotation_send()
        self.assertEqual(result["type"], "ir.actions.act_window")
        self.assertEqual(result["res_model"], "mail.compose.message")

    def test_sync_sale_order_lines(self):
        """When changing combination, correctly re-sync sale order lines."""
        booking_id = self.create_booking(combination_id=self.many_combinations[0].id)
        for combination_id in self.many_combinations:
            booking_id.combination_id = combination_id
            # One booking as order line, two resources as order lines.
            self.assertEqual(len(booking_id.sale_order_line_ids), 3)
            # Assuming that products are unique for each resource (which they
            # are in this scenario), we expect to find sale order lines with
            # products identical to the products of the resources in the
            # combination.
            resources = booking_id.combination_id.resource_ids
            resource_products = resources.mapped("product_id")
            result = (
                booking_id.sale_order_line_ids.mapped("product_id")
                - booking_id.product_id
            )
            self.assertEqual(resource_products, result)

    def test_sync_sale_order_lines_dont_sync_existing_lines(self):
        """When changing to a combination that has an identical resource to the
        previous combination, do not change that resource's order line.
        """
        booking_id = self.create_booking(combination_id=self.many_combinations[0].id)
        booking_id.sale_order_line_ids[1].price_unit = 999
        booking_id.combination_id = self.many_combinations[1]
        self.assertEqual(booking_id.sale_order_line_ids[1].price_unit, 999)
        # Remove and re-add the line.
        booking_id.combination_id = self.many_combinations[-1]
        booking_id.combination_id = self.many_combinations[1]
        self.assertNotEqual(booking_id.sale_order_line_ids[1].price_unit, 999)

    def test_sync_sale_order_lines_dont_remove_unrelated_product(self):
        """Unrelated products are not removed on sync."""
        booking_id = self.create_booking(combination_id=self.many_combinations[0].id)
        template_id = self.env["product.template"].create(
            {
                "name": "Test Unrelated Product",
            }
        )
        product_id = template_id.product_variant_id
        self.env["sale.order.line"].create(
            {
                "product_id": product_id.id,
                "order_id": booking_id.sale_order_id.id,
            }
        )
        booking_id.combination_id = self.many_combinations[-1]
        self.assertIn(product_id, booking_id.sale_order_line_ids.mapped("product_id"))

    def test_sync_sale_order_lines_resources_share_product(self):
        product_id = self.many_combinations[0].resource_ids[0].product_id
        self.many_combinations[0].resource_ids[1].product_id = product_id
        booking_id = self.create_booking(combination_id=self.many_combinations[0].id)
        # Two resources share same product, ergo length is 2 instead of 3.
        self.assertEqual(len(booking_id.sale_order_line_ids), 2)
        # Correctly remove the shared sale order line.
        booking_id.combination_id = self.many_combinations[-1]
        self.assertEqual(len(booking_id.sale_order_line_ids), 3)
        self.assertNotIn(
            product_id, booking_id.sale_order_line_ids.mapped("product_id")
        )

    def test_sync_sale_order_lines_no_product(self):
        """Expect regular behaviour (i.e., no exceptions) when some resources
        have no products.
        """
        # Get every other resource
        resources = self.many_resources[::2]
        resources.write({"product_id": False})
        booking_id = self.create_booking(combination_id=self.many_combinations[0].id)
        for combination_id in self.many_combinations:
            booking_id.combination_id = combination_id
