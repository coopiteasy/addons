# -*- coding: utf-8 -*-

from openerp import models, fields, api


class OpeningHoursDay(models.Model):
    _name = 'activity.opening.hours.day'
    _order = 'dayofweek,opening_time'

    opening_hours_id = fields.Many2one(
        comodel_name='activity.opening.hours',
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
        string='opening',
        help='format: HH:mm',
        required=True,
    )
