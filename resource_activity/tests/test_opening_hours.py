# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from openerp.exceptions import ValidationError
import datetime as dt


class TestOpeningHours(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestOpeningHours, cls).setUpClass()

    def test_get_opening_hours_winter_2018(self):
        time = dt.datetime(2019, 1, 5, 12, 0)
        location = self.env.ref('resource_planning.main_location')
        searched_oh = (
            self.env['activity.opening.hours']
                .get_opening_hours(location, time)
        )

        data_oh = self.env.ref(
            'resource_activity.activity_opening_hours_winter_2018'
        )
        self.assertEqual(searched_oh.id, data_oh.id)

    def test_get_opening_hours_summer_2019(self):
        time = dt.datetime(2019, 7, 5, 12, 23)
        location = self.env.ref('resource_planning.main_location')
        searched_oh = (
            self.env['activity.opening.hours']
                .get_opening_hours(location, time)
        )

        data_oh = self.env.ref(
            'resource_activity.activity_opening_hours_summer_2019'
        )
        self.assertEqual(searched_oh.id, data_oh.id)

    def test_get_opening_hours_holidays(self):
        time = dt.datetime(2018, 12, 25, 12, 0)
        location = self.env.ref('resource_planning.main_location')
        searched_oh = (
            self.env['activity.opening.hours']
                .get_opening_hours(location, time)
        )

        data_oh = self.env.ref(
            'resource_activity.activity_opening_hours_christmas_2018'
        )
        self.assertEqual(searched_oh.id, data_oh.id)

    def test_get_opening_hours_summer_1969(self):
        # Purple Haze
        time = dt.datetime(1969, 8, 18, 8, 32)
        location = self.env.ref('resource_planning.main_location')

        with self.assertRaises(ValidationError):
            (self.env['activity.opening.hours']
                 .get_opening_hours(location, time))

    def test_opening_hours_day_is_open(self):
        day = self.env.ref('resource_activity.activity_opening_hours_day_christmas_2018')

        time = dt.datetime(2018, 12, 25, 11, 11)
        self.assertTrue(day.is_open(time))

        time = dt.datetime(2018, 12, 25, 21, 21)
        self.assertFalse(day.is_open(time))

        time = dt.datetime(2018, 12, 24, 11, 11)
        self.assertFalse(day.is_open(time))

        time = dt.datetime(2018, 12, 24, 21, 11)
        self.assertFalse(day.is_open(time))

    def test_is_location_open_winter_2018(self):
        oh = self.env['activity.opening.hours']
        location = self.env.ref('resource_planning.main_location')

        friday_1 = dt.datetime(2019, 1, 4, 12, 0)
        self.assertTrue(oh.is_location_open(location, friday_1))

        friday_2 = dt.datetime(2019, 1, 4, 13, 15)
        self.assertFalse(oh.is_location_open(location, friday_2))

        saturday = dt.datetime(2019, 1, 5, 12, 0)
        self.assertFalse(oh.is_location_open(location, saturday))

    def test_is_location_open_summer_1969(self):
        oh = self.env['activity.opening.hours']
        time = dt.datetime(1969, 8, 18, 8, 32)
        location = self.env.ref('resource_planning.main_location')

        with self.assertRaises(ValidationError):
            oh.is_location_open(location, time)

    def test_check_overlapping_records(self):
        oh = self.env['activity.opening.hours']
        location = self.env.ref('resource_planning.main_location')
        oh.create({
            'name': 'test opening reference',
            'location_id': location.id,
            'start': '2000-02-01',
            'end': '2000-03-01',
            'is_holiday': False,
        })

        with self.assertRaises(ValidationError):
            oh.create({
                'name': 'test opening hours',
                'location_id': location.id,
                'start': '2000-02-02',
                'end': '2000-02-03',
                'is_holiday': False,
            })
        with self.assertRaises(ValidationError):
            oh.create({
                'name': 'test opening hours',
                'location_id': location.id,
                'start': '2000-01-01',
                'end': '2000-02-10',
                'is_holiday': False,
            })
        with self.assertRaises(ValidationError):
            oh.create({
                'name': 'test opening hours',
                'location_id': location.id,
                'start': '2000-01-01',
                'end': '2000-03-10',
                'is_holiday': False,
            })
        with self.assertRaises(ValidationError):
            oh.create({
                'name': 'test opening hours',
                'location_id': location.id,
                'start': '2000-02-10',
                'end': '2000-03-10',
                'is_holiday': False,
            })

    def test_check_time_format(self):
        ohd = self.env['activity.opening.hours.day']
        oh = self.env.ref('resource_activity'
                          '.activity_opening_hours_christmas_2018')

        ohd.create({
            'opening_hours_id': oh.id,
            'dayofweek': '0',
            'opening_time': '12:34',
            'closing_time': '13:45',
        })

        with self.assertRaises(ValidationError):
            ohd.create({
                'opening_hours_id': oh.id,
                'dayofweek': '0',
                'opening_time': '1234',
                'closing_time': '13:45',
            })
        with self.assertRaises(ValidationError):
            ohd.create({
                'opening_hours_id': oh.id,
                'dayofweek': '0',
                'opening_time': '1234',
                'closing_time': '13:45',
            })
        with self.assertRaises(ValidationError):
            ohd.create({
                'opening_hours_id': oh.id,
                'dayofweek': '0',
                'opening_time': '12346',
                'closing_time': '13:45',
            })
        with self.assertRaises(ValidationError):
            ohd.create({
                'opening_hours_id': oh.id,
                'dayofweek': '0',
                'opening_time': '12:3',
                'closing_time': '13:45',
            })
        with self.assertRaises(ValidationError):
            ohd.create({
                'opening_hours_id': oh.id,
                'dayofweek': '0',
                'opening_time': '1234',
                'closing_time': '13:aa',
            })
