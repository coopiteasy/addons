# Copyright 2024 Coop IT Easy <https://coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EventTrackSpeakerMealDate(models.Model):
    _name = "event.track.speaker.meal.date"
    _description = "Track Speaker Meal Date"

    speaker_id = fields.Many2one("event.track.speaker", string="Speaker")
    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )
    date = fields.Date()

    @api.constrains("date")
    def _constrain_date_valid(self):
        for meal_date in self:
            if (
                meal_date.date < meal_date.event_id.date_begin.date()
                or meal_date.date > meal_date.event_id.date_end.date()
            ):
                raise ValidationError(
                    "Meal date must match the event dates of the speaker."
                )