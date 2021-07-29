# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.tests import common
from datetime import datetime, timedelta


class TestResourceActivity(common.TransactionCase):
    def setUp(self):
        super(TestResourceActivity, self).setUp()
        self.partner_demo = self.browse_ref("base.partner_demo")
        self.bike_category = self.browse_ref(
            "resource_planning.resource_category_bike_demo"
        )
        self.bike_product = self.browse_ref(
            "resource_activity.product_product_bike_rent_demo"
        )
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.activity_type = self.browse_ref(
            "resource_activity.resource_activity_type_tour_demo"
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

    def test_activity_w_booked_resources(self):
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
                "registrations": [(0, 0, registration)],
            }
        )

        activity.search_all_resources()
        activity.reserve_needed_resource()

        activity.create_sale_order()
        sale_order = activity.sale_orders
        self.assertEquals(len(sale_order.order_line), 1)
        self.assertEquals(activity.sale_orders.amount_total, 115)
