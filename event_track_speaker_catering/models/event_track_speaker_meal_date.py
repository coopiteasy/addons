# Copyright 2024 Coop IT Easy <https://coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventTrackSpeakerMealDate(models.Model):
    _name = "event.track.speaker.meal.date"
    _description = "Track Speaker Meal Date"

    def _default_date(self):
        event_id = self.env.context.get("event_id")
        if event_id:
            event = self.env["event.event"].browse(event_id)
            return event.date_begin
        return None

    speaker_id = fields.Many2one("event.track.speaker", string="Speaker")
    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )
    date = fields.Date(default=_default_date)
    quantity = fields.Integer(default=1)

    @api.constrains("date")
    def _constrain_date_valid(self):
        for meal_date in self:
            if (
                meal_date.date < meal_date.event_id.date_begin.date()
                or meal_date.date > meal_date.event_id.date_end.date()
            ):
                raise ValidationError(
                    _("Meal date must match the event dates of the speaker.")
                )
