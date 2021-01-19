# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.tests import common


class TestResourcePlanning(common.TransactionCase):
    def setUp(self):
        super(TestResourcePlanning, self).setUp()
        self.main_location = self.browse_ref("resource_planning.main_location")
        self.alloc_1 = self.browse_ref(
            "resource_planning.resource_allocation_1_demo"
        )
        self.alloc_2 = self.browse_ref(
            "resource_planning.resource_allocation_2_demo"
        )
        self.alloc_3 = self.browse_ref(
            "resource_planning.resource_allocation_3_demo"
        )
        self.alloc_4 = self.browse_ref(
            "resource_planning.resource_allocation_4_demo"
        )
        self.alloc_5 = self.browse_ref(
            "resource_planning.resource_allocation_5_demo"
        )
        self.alloc_6 = self.browse_ref(
            "resource_planning.resource_allocation_6_demo"
        )

    def test_get_allocations(self):
        allocation_obj = self.env["resource.allocation"]

        allocations = allocation_obj.get_allocations(
            date_start="2020-11-23 14:30",
            date_end="2020-11-23 16:00",
            location=self.main_location,
        )
        self.assertIn(self.alloc_1, allocations)
        self.assertIn(self.alloc_3, allocations)
        self.assertIn(self.alloc_6, allocations)

        allocations = allocation_obj.get_allocations(
            date_start="2020-11-23 19:30",
            date_end="2020-11-23 20:00",
            location=self.main_location,
        )
        self.assertIn(self.alloc_2, allocations)

        allocations = allocation_obj.get_allocations(
            date_start="2020-11-24 19:30",
            date_end="2020-11-24 20:00",
            location=self.main_location,
        )
        self.assertEquals(len(allocations), 0)

    def test_get_available_categories(self):
        category_obj = self.env["resource.category"]

        categories = category_obj.get_available_categories(
            date_start="2020-11-23 14:30",
            date_end="2020-11-23 16:00",
            location=self.main_location,
        )
        self.assertEquals({}, categories)

        categories = category_obj.get_available_categories(
            date_start="2020-11-23 19:30",
            date_end="2020-11-23 20:00",
            location=self.main_location,
        )
        self.assertEquals({1: 1, 2: 1}, categories)

        categories = category_obj.get_available_categories(
            date_start="2020-11-23 17:00",
            date_end="2020-11-23 17:30",
            location=self.main_location,
        )
        self.assertEquals({1: 2}, categories)

        categories = category_obj.get_available_categories(
            date_start="2020-11-24 19:30",
            date_end="2020-11-24 20:00",
            location=self.main_location,
        )
        self.assertEquals({1: 2, 2: 1}, categories)
