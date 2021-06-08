# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import test_base


class TestSaleOrder(test_base.TestResourceActivityBase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        company = self.env.user.company_id

        self.default_terms = self.env["res.company.note"].create(
            {
                "company_id": company.id,
                "name": "Default terms",
                "content": "Default company terms content",
            }
        )
        company.sale_note_html_id = self.default_terms

        self.location_terms = self.env["res.company.note"].create(
            {
                "company_id": company.id,
                "name": "Location terms",
                "content": "Location_specific terms content",
            }
        )
        self.env["resource.location.terms"].create(
            {
                "location_id": self.main_location.id,
                "activity_type_id": self.activity_type.id,
                "note_id": self.location_terms.id,
            }
        )

    def test_default_note_assigned_to_sale_order(self):
        some_activity = self.env["resource.activity.type"].create(
            {"name": "Some Test Activity"}
        )
        activity = self.env["resource.activity"].create(
            {
                "partner_id": self.partner_demo.id,
                "date_start": "2020-11-24 19:30",
                "date_end": "2020-11-24 20:00",
                "location_id": self.main_location.id,
                "activity_type": some_activity.id,
                "need_guide": True,
                "guide_product_id": self.guide_product.id,
            }
        )
        activity.create_sale_order()
        # should be only one sale order
        sale_order = activity.sale_orders
        self.assertEquals(sale_order.note_html_id, self.default_terms)

    def test_location_note_assigned_to_sale_order(self):
        activity = self.env["resource.activity"].create(
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
        # should be only one sale order
        sale_order = activity.sale_orders
        self.assertEquals(sale_order.note_html_id, self.location_terms)
