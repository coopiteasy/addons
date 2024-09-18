# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from datetime import datetime

from odoo import api, fields, models


class EventTrackDate(models.Model):
    _name = "event.track.date"
    _description = "Track dates"

    track_id = fields.Many2one("event.track")
    datetime = fields.Datetime(string="Date and time")
    date = fields.Date(compute="_compute_date_and_time")
    hour = fields.Float(string="Hours", compute="_compute_date_and_time")

    @api.depends("date")
    def _compute_date_and_time(self):
        for track_date in self:
            if track_date.datetime:
                track_date.date = track_date.datetime.date()
                track_date.hour = (
                    fields.Datetime.context_timestamp(
                        self.env.user, track_date.datetime
                    )
                    - fields.Datetime.context_timestamp(
                        self.env.user,
                        datetime.combine(track_date.date, datetime.min.time()),
                    ).replace(hour=0, minute=0, second=0)
                ).total_seconds() / 3600
            else:
                track_date.date = False
                track_date.hour = False
