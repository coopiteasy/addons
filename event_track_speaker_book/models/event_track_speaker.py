# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrackSpeaker(models.Model):
    _inherit = "event.track.speaker"

    book_ids = fields.Many2many("event.track.speaker.book", string="Books")