# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, fields, models


class EventTrackSpeakerMealDate(models.Model):
    _name = "event.track.speaker.meal.date"
    _description = "Track Speaker Meal Date"

    speaker_id = fields.Many2one("event.track.speaker", string="Speaker")
    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )

    @api.depends("event_id.date_begin")
    def get_event_begin_date(self):
        return self.event_id.date_begin

    date = fields.Date(default=datetime.strftime("2020-01-01"))
