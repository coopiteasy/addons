# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timedelta

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
        cls.resource_id = cls.env["resource.resource"].create(
            {
                "name": "Test Resource",
                "resource_type": "material",
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
    ):
        return self.env["resource.booking"].create(
            {
                "partner_id": partner_id or self.partner_id.id,
                "type_id": booking_type_id or self.booking_type_id.id,
                "product_id": product_id or self.product_id.id,
                "start": target_date or self.target_date,
                "duration": duration or 1,
            }
        )

    def test_create_sale_order(self):
        """When creating a resource.booking, also create and link a sale order."""
        booking_id = self.create_booking()
        self.assertTrue(booking_id.sale_order_id)
        self.assertEqual(booking_id.sale_order_line_ids[0].product_id, self.product_id)

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
