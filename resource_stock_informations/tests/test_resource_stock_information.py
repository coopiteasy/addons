# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from openerp.fields import Date, Datetime
from openerp.tests import common
from openerp.exceptions import ValidationError


class TestResourceStockInformation(common.TransactionCase):
    def setUp(self):
        super(TestResourceStockInformation, self).setUp()
        self.allocation_obj = self.env["resource.allocation"]

        self.partner_demo = self.browse_ref("base.partner_demo")
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.bike_1 = self.browse_ref(
            "resource_planning.resource_resource_bike_1_demo"
        )
        self.bike_2 = self.browse_ref(
            "resource_planning.resource_resource_bike_2_demo"
        )
        self.ebike_1 = self.browse_ref(
            "resource_planning.resource_resource_ebike_1_demo"
        )

        now = datetime.now()
        tomorrow_10am = now.replace(hour=10, minute=0) + timedelta(days=1)
        tomorrow_12am = tomorrow_10am + timedelta(hours=2)
        self.alloc_r1_1 = self.allocation_obj.create(
            {
                "resource_id": self.bike_1.id,
                "date_start": Datetime.to_string(tomorrow_10am),
                "date_end": Datetime.to_string(tomorrow_12am),
                "state": "booked",
                "location": self.main_location.id,
            }
        )

        next_week_10am = now.replace(hour=10, minute=0) + timedelta(days=7)
        next_week_12am = next_week_10am + timedelta(hours=2)
        self.alloc_r1_2 = self.allocation_obj.create(
            {
                "resource_id": self.bike_1.id,
                "date_start": Datetime.to_string(next_week_10am),
                "date_end": Datetime.to_string(next_week_12am),
                "state": "booked",
                "location": self.main_location.id,
            }
        )

        d_plus_2_10am = now.replace(hour=10, minute=0) + timedelta(days=2)
        d_plus_2_12am = d_plus_2_10am + timedelta(hours=2)
        self.alloc_r2_1 = self.allocation_obj.create(
            {
                "resource_id": self.bike_2.id,
                "date_start": Datetime.to_string(d_plus_2_10am),
                "date_end": Datetime.to_string(d_plus_2_12am),
                "state": "booked",
                "location": self.main_location.id,
            }
        )
        d_plus_2_2pm = d_plus_2_10am + timedelta(hours=4)
        d_plus_2_4pm = d_plus_2_10am + timedelta(hours=6)
        self.alloc_r2_2 = self.allocation_obj.create(
            {
                "resource_id": self.bike_2.id,
                "date_start": Datetime.to_string(d_plus_2_2pm),
                "date_end": Datetime.to_string(d_plus_2_4pm),
                "state": "booked",
                "location": self.main_location.id,
            }
        )

    def test_resource_removed_from_stock(self):
        wiz_action = self.bike_1.action_remove_from_stock()
        wiz = self.env[wiz_action["res_model"]].browse(wiz_action["res_id"])
        today = Date.today()
        reason = "sold"
        selling_price = 3
        invoice_ref = "REF001"

        wiz.write(
            {
                "stock_removal_date": today,
                "stock_removal_reason": reason,
                "selling_price": selling_price,
                "sale_invoice_ref": invoice_ref,
                "force_remove": True,
            }
        )
        wiz.remove_resource_from_stock()

        self.assertTrue(self.bike_1.removed_from_stock)
        self.assertEquals(self.bike_1.state, "unavailable")
        self.assertEquals(self.bike_1.stock_removal_date, today)
        self.assertEquals(self.bike_1.stock_removal_reason, reason)
        self.assertEquals(self.bike_1.selling_price, selling_price)
        self.assertEquals(self.bike_1.sale_invoice_ref, invoice_ref)

    def test_replace_resource_by_available_resource(self):
        wiz = self.env["resource.stock.removal.wizard"].create(
            {"resource_id": self.bike_1.id}
        )
        self.assertIn(
            self.bike_2.id,
            wiz.candidate_resource_ids.ids,
            "Bike 2 is available to replace bike 1",
        )
        self.assertNotIn(
            self.ebike_1.id,
            wiz.candidate_resource_ids.ids,
            "Ebike 1 is not available to replace bike 1",
        )

        # Cannot remove resource from stock if future allocations exist
        with self.assertRaises(ValidationError):
            wiz.button_remove_resource_from_stock()

        # Missing replacing_resource_id raises Validation Error
        with self.assertRaises(ValidationError):
            wiz.button_remove_resource_from_stock_and_fix_allocations()

        wiz.replacing_resource_id = self.bike_2
        wiz.stock_removal_reason = "other"
        wiz.button_remove_resource_from_stock_and_fix_allocations()
        self.assertTrue(
            all(
                (
                    ra.resource_id == self.bike_2
                    for ra in wiz.allocations_to_fix_ids
                )
            ),
            "Future allocations of bike_1 are replaced by bike2",
        )

    def test_no_resource_available_for_replacement(self):
        self.alloc_r2_1.write(
            {  # create conflict
                "date_start": self.alloc_r1_1.date_start,
                "date_end": self.alloc_r1_1.date_end,
            }
        )
        wiz = self.env["resource.stock.removal.wizard"].create(
            {"resource_id": self.bike_1.id}
        )
        self.assertFalse(
            wiz.candidate_resource_ids,
            "No candidates available for replacement",
        )

    def test_no_allocations_to_replace(self):
        bike_3 = self.bike_1.copy()
        wiz = self.env["resource.stock.removal.wizard"].create(
            {"resource_id": bike_3.id}
        )
        self.assertFalse(
            wiz.allocations_to_fix_ids,
            "Nothing to replace",
        )
        # Missing stock_removal_reason raises Validation Error
        with self.assertRaises(ValidationError):
            wiz.button_remove_resource_from_stock()
        wiz.stock_removal_reason = "other"

        wiz.button_remove_resource_from_stock()

    def test_force_remove_if_no_candidates(self):
        self.alloc_r2_1.write(
            {  # create conflict
                "date_start": self.alloc_r1_1.date_start,
                "date_end": self.alloc_r1_1.date_end,
            }
        )
        wiz = self.env["resource.stock.removal.wizard"].create(
            {"resource_id": self.bike_1.id, "stock_removal_reason": "other"}
        )
        self.assertFalse(
            wiz.candidate_resource_ids,
            "No candidates available for replacement",
        )
        wiz.force_remove = True
        wiz.button_remove_resource_from_stock()
