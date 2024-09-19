# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventTrackDate(models.Model):
    _name = "event.track.date"
    _description = "Track dates"

    def _default_datetime(self):
        event_id = self.env.context.get("event_id")
        if event_id:
            event = self.env["event.event"].browse(event_id)
            return event.date_begin
        return None

    track_id = fields.Many2one("event.track")
    event_id = fields.Many2one(related="track_id.event_id")
    datetime = fields.Datetime(string="Date and time", default=_default_datetime)
    date = fields.Date(compute="_compute_date_and_time")
    hour = fields.Float(string="Hours", compute="_compute_date_and_time")

    @api.depends("datetime")
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

    @api.constrains("datetime")
    def _constrain_datetime_valid(self):
        for track in self:
            if (
                track.datetime < track.event_id.date_begin
                or track.datetime > track.event_id.date_end
            ):
                raise ValidationError(
                    _("Date must match the event dates of the track.")
                )
