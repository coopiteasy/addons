# Copyright 2024 Coop IT Easy <https://coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    book_ids = fields.Many2many(
        comodel_name="event.track.speaker.book",
        string="Books",
    )

    @api.onchange("speaker_ids")
    def get_book_domain(self):
        for rec in self:
            speakers_book_ids = rec.speaker_ids._origin.mapped("book_ids").mapped("id")
            return {"domain": {"book_ids": [("id", "in", speakers_book_ids)]}}
