# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    book_ids = fields.Many2many(
        comodel_name="event.track", compute="_compute_books", string="Books"
    )

    @api.depends("speaker_ids.book_ids")
    def _compute_books(self):
        books = []
        for speaker in self.speaker_ids:
            books += speaker.book_ids
