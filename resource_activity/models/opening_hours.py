# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ActivityOpeningHours(models.Model):
    _name = 'activity.opening.hours'

    @api.model
    def _get_default_location(self):
        location = self.env.user.resource_location
        if not location:
            main_location = self.env.ref('resource_planning.main_location', False)
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
        string='Is Holiday Opening Hours',
        default=False,
    )
    opening_day_ids = fields.One2many(
        comodel_name='activity.opening.hours.day',
        inverse_name='opening_hours_id',
        string='Opening Days'
    )

# at least one opening.hours.day set for each week day
# at most one holiday period set for each time
# at most one non holiday period set for each time
# generate next years summer
