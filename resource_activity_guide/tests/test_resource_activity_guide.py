# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.addons.resource_activity.tests.test_resource_activity import (
    TestResourceActivity,
)


class TestResourceActivityGuide(TestResourceActivity):
    def setUp(self):
        super(TestResourceActivityGuide, self).setUp()
        self.guide_partner_1 = self.browse_ref(
            "resource_activity_guide.res_partner_friendly_guide_demo"
        )
        self.guide_partner_2 = self.browse_ref(
            "resource_activity_guide.res_partner_mean_guide_demo"
        )
        self.guide_product = self.browse_ref(
            "resource_activity_guide.guide_product_product_demo"
        )

    def test_create_guide_only_sale_order_no_guides(self):
        activity_obj = self.env["resource.activity"]

        activity = activity_obj.create(
            {
                "partner_id": self.partner_demo.id,
                "date_start": "2020-11-24 19:30",
                "date_end": "2020-11-24 20:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
                "need_guide": True,
                "guide_product_id": self.guide_product.id,
            }
        )
        activity.create_sale_order()
        sale_order = activity.sale_orders
        self.assertEquals(len(sale_order.order_line), 1)
        self.assertEquals(activity.sale_orders.amount_total, 0)

    def test_create_guide_only_sale_order_with_guides(self):
        activity_obj = self.env["resource.activity"]

        activity = activity_obj.create(
            {
                "partner_id": self.partner_demo.id,
                "date_start": "2020-11-24 19:30",
                "date_end": "2020-11-24 20:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
                "need_guide": True,
                "guide_product_id": self.guide_product.id,
                "guides": [
                    (4, self.guide_partner_1.id, 0),
                    (4, self.guide_partner_2.id, 0),
                ],
            }
        )
        activity.create_sale_order()
        sale_order = activity.sale_orders
        self.assertEquals(len(sale_order.order_line), 1)
        self.assertEquals(activity.sale_orders.amount_total, 230)

    def test_create_guide_only_sale_order_with_guides_and_registrations(self):
        activity_obj = self.env["resource.activity"]

        activity = activity_obj.create(
            {
                "partner_id": self.partner_demo.id,
                "date_start": "2020-11-24 19:30",
                "date_end": "2020-11-24 20:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
                "need_guide": True,
                "guide_product_id": self.guide_product.id,
                "guides": [
                    (4, self.guide_partner_1.id, 0),
                    (4, self.guide_partner_2.id, 0),
                ],
                "registrations": [
                    (
                        0,
                        0,
                        {
                            "attendee_id": self.partner_demo.id,
                            "quantity": 2,
                            "quantity_needed": 0,
                            "booking_type": "booked",
                            "state": "booked",
                            "bring_bike": True,
                        },
                    )
                ],
            }
        )
        activity.create_sale_order()
        sale_order = activity.sale_orders
        self.assertEquals(len(sale_order.order_line), 1)
        self.assertEquals(activity.sale_orders.amount_total, 230)
