# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import datetime as dt
import pytz


class ActivityOpeningHours(models.Model):
    _name = 'activity.opening.hours'

    @api.model
    def _get_default_location(self):
        location = self.env.user.resource_location
        if not location:
            main_location = self.env.ref('resource_planning.main_location',
                                         False)
            return main_location if main_location else False
        return location

    name = fields.Char(
        string='Name',
    )
    location_id = fields.Many2one(
        comodel_name='resource.location',
        string='Location',
        default=_get_default_location,
        required=True,
    )
    start = fields.Date(
        string='Validity Start Date',
        required=True,
    )
    end = fields.Date(
        string='Validity End Date',
        required=True,
    )
    is_holiday = fields.Boolean(
        string='Is Holiday',
        default=False,
    )
    opening_day_ids = fields.One2many(
        comodel_name='activity.opening.hours.day',
        inverse_name='opening_hours_id',
        string='Opening Days'
    )

    @api.one
    @api.constrains('location_id', 'start', 'end', 'is_holiday')
    def check_overlapping_records(self):
        other_oh = self.search([('location_id', '=', self.location_id.id),
                                ('is_holiday', '=', self.is_holiday),
                                ('id', '!=', self.id)])

        for oh in other_oh:
            if not (oh.end <= self.start or oh.start >= self.end):
                raise ValidationError(_(
                    '% opening hours are overlapping with % opening hours'
                ) % (self.name, oh.name))

    @api.model
    def get_opening_hours(self, location, time):
        opening_hours = self.search(
            [('location_id', '=', location.id),
             ('start', '<=', time),
             ('end', '>', time)],
            order='is_holiday desc',  # (null), True, False
        )

        if not opening_hours:
            raise ValidationError(_(
                'No opening hours set for %s') % time
            )
        return opening_hours[0]

    def _localize(self, date):
        tz = pytz.timezone(self._context['tz']) if self._context['tz'] else pytz.utc
        return pytz.utc.localize(date).astimezone(tz)

    @api.model
    def is_location_open(self, location, time):
        if type(time) in (str, unicode):
            time = dt.datetime.strptime(time, DEFAULT_SERVER_DATETIME_FORMAT)
            time = self._localize(time)

        opening_hours = self.get_opening_hours(location, time)
        return opening_hours.opening_day_ids.is_open(time)
