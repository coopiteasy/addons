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
        return [(6, 0, location.id)]

    name = fields.Char(
        string='Name',
    )
    location_ids = fields.Many2many(
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
    active = fields.Boolean(
        default=True,
    )

    @api.model
    def get_opening_hours(self, location, time):
        opening_hours = self.search(
            [('location_ids', 'in', [location.id]),
             ('start', '<=', time),
             ('end', '>', time)],
            order='is_holiday desc',  # (null), True, False
        )

        if not opening_hours:
            raise ValidationError(_(
                'No opening hours set for %s') % time
            )
        if len(opening_hours) >= 2:
            if opening_hours[0].is_holiday and opening_hours[1].is_holiday:
                raise ValidationError(_(
                    'Two holiday opening hours set for %s') % time)
            elif not opening_hours[0].is_holiday and not opening_hours[1].is_holiday:
                raise ValidationError(_(
                    'Two opening hours set for %s') % time)

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
