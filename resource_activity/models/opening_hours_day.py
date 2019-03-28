# -*- coding: utf-8 -*-

from openerp import models, fields, api


class OpeningHoursDay(models.Model):
    _name = 'activity.opening.hours.day'
    _order = 'dayofweek,opening_time'

    opening_hours_id = fields.Many2one(
        comodel_name='activity.opening.hours',
        inverse_name='opening_day_ids',
        string='Opening Hours',
        required=True,
    )
    dayofweek = fields.Selection(
        selection=[('0', 'Monday'),
                   ('1', 'Tuesday'),
                   ('2', 'Wednesday'),
                   ('3', 'Thursday'),
                   ('4', 'Friday'),
                   ('5', 'Saturday'),
                   ('6', 'Sunday')],
        string='Day of Week',
        required=True,
    )
    opening_time = fields.Char(
        string='Opening Time',
        help='format: HH:mm',
        required=True,
    )
    closing_time = fields.Char(
        string='Closing Time',
        help='format: HH:mm',
        required=True,
    )

    def compute_hour_minute(self, time):
        """time is a string HH:mm"""
        return tuple(int(x) for x in time.split(':'))

    @api.multi
    def is_open(self, time):
        for day in self:
            shour, smin = self.compute_hour_minute(day.opening_time)
            opening_time = time.replace(hour=shour, minute=smin)
            ehour, emin = self.compute_hour_minute(day.closing_time)
            closing_time = time.replace(hour=ehour, minute=emin)

            same_weekday = time.weekday() == int(day.dayofweek)
            within_hours = opening_time <= time <= closing_time

            if same_weekday and within_hours:
                return True
        return False
