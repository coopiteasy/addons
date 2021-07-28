# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.addons.resource_activity.tests.test_resource_activity import (
    TestResourceActivity,
)
from datetime import datetime, timedelta


class TestResourceActivityDelivery(TestResourceActivity):
    def setUp(self):
        super(TestResourceActivityDelivery, self).setUp()
        self.delivery_product = self.browse_ref("resource_activity_delivery.product_product_delivery_demo")

    def test_delivery_lines_set_in_sale_order(self):
        date_start = datetime.now()
        date_end = date_start + timedelta(hours=2)

        registration = {
            "attendee_id": self.partner_demo.id,
            "quantity": 2,
            "quantity_needed": 2,
            "booking_type": "booked",
            "resource_category": self.bike_category.id,
            "product_id": self.bike_product.id,

        }
        activity = self.env["resource.activity"].create(
            {
                "date_start": date_start,
                "date_end": date_end,
                # set by _onchange_allocation_start in real life
                "resource_allocation_start": date_start,
                # set by _onchange_allocation_end in real life
                "resource_allocation_end": date_end,
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
                "need_delivery": True,
                "delivery_product_id": self.delivery_product.id,
                "registrations": [(0, 0, registration)],
            }
        )

        activity.search_all_resources()
        activity.reserve_needed_resource()

        activity.create_sale_order()
        sale_order = activity.sale_orders
        self.assertEquals(len(sale_order.order_line), 2)
        self.assertEquals(activity.sale_orders.amount_total, 120)
