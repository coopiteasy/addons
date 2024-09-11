# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrackSpeakerBook(models.Model):
    _name = "event.track.speaker.meal.date"
    _description = "Track Speaker Meal Date"

    speaker_id = fields.Many2one("event.track.speaker", string="Speaker")
    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )
    date = fields.Date()
