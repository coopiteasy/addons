# Copyright 2024 Coop IT Easy <https://coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrackSpeaker(models.Model):
    _inherit = "event.track.speaker"

    meal_date_ids = fields.One2many(
        "event.track.speaker.meal.date", "speaker_id", string="Meal Date"
    )
