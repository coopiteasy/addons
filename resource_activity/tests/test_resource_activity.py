# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.tests import common


class TestResourceActivity(common.TransactionCase):
    def setUp(self):
        super(TestResourceActivity, self).setUp()
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
