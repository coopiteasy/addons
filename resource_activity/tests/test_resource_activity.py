# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.tests import common


class TestResourceActivity(common.TransactionCase):
    def setUp(self):
        super(TestResourceActivity, self).setUp()
        self.partner_demo = self.env.ref("base.partner_demo")
        self.guide_partner_1 = self.browse_ref(
            "resource_activity.res_partner_friendly_guide_demo"
        )
        self.guide_partner_2 = self.browse_ref(
            "resource_activity.res_partner_mean_guide_demo"
        )
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.activity_type = self.browse_ref(
            "resource_activity.resource_activity_type_tour_demo"
        )
        self.guide_product = self.browse_ref(
            "resource_activity.guide_product_product_demo"
        )

    def test_compute_available_resources(self):
        activity_obj = self.env["resource.activity"]
        activity = activity_obj.create(
            {
                "date_start": "2020-11-23 14:30",
                "date_end": "2020-11-23 16:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        self.assertEquals(len(activity.available_category_ids), 0)

        activity = activity_obj.create(
            {
                "date_start": "2020-11-23 19:30",
                "date_end": "2020-11-23 20:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        categories = {
            av_categ.category_id.id: av_categ.nb_resources
            for av_categ in activity.available_category_ids
        }
        self.assertEquals({1: 1, 2: 1}, categories)

        activity = activity_obj.create(
            {
                "date_start": "2020-11-23 17:00",
                "date_end": "2020-11-23 17:30",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        categories = {
            av_categ.category_id.id: av_categ.nb_resources
            for av_categ in activity.available_category_ids
        }
        self.assertEquals({1: 2}, categories)

        activity = activity_obj.create(
            {
                "date_start": "2020-11-24 19:30",
                "date_end": "2020-11-24 20:00",
                "location_id": self.main_location.id,
                "activity_type": self.activity_type.id,
            }
        )
        categories = {
            av_categ.category_id.id: av_categ.nb_resources
            for av_categ in activity.available_category_ids
        }
        self.assertEquals({1: 2, 2: 1}, categories)

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
        self.assertEquals(activity.sale_orders.amount_total, 200)

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
        self.assertEquals(activity.sale_orders.amount_total, 200)
