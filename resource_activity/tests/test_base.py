# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.tests import common


class TestResourceActivityBase(common.TransactionCase):
    def setUp(self):
        super(TestResourceActivityBase, self).setUp()
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
