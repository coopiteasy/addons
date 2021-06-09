# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.fields import Date
from openerp.tests import common


class TestResourceStockInformation(common.TransactionCase):
    def setUp(self):
        super(TestResourceStockInformation, self).setUp()
        self.partner_demo = self.browse_ref("base.partner_demo")
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.bike_1 = self.browse_ref(
            "resource_planning.resource_resource_bike_1_demo"
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
            }
        )
        wiz.remove_resource_from_stock()

        self.assertTrue(self.bike_1.removed_from_stock)
        self.assertEquals(self.bike_1.state, "unavailable")
        self.assertEquals(self.bike_1.stock_removal_date, today)
        self.assertEquals(self.bike_1.stock_removal_reason, reason)
        self.assertEquals(self.bike_1.selling_price, selling_price)
        self.assertEquals(self.bike_1.sale_invoice_ref, invoice_ref)
