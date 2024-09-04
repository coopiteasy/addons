# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrackSpeakerBook(models.Model):
    _name = "event.track.speaker.book"
    _description = "Track Speaker Book"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Title")
    author_id = fields.Many2many(comodel_name="res.partner", string="Authors")
    editor_id = fields.Many2one(comodel_name="res.partner", string="Editor")
    user_id = fields.Many2one("res.users", string="Referent")
    speaker_ids = fields.Many2many("event.track.speaker", string="Speakers")
    status = fields.Selection(
        selection=[
            ("asked", "Asked"),
            ("received", "Received"),
            ("reading", "Reading"),
            ("done", "Done"),
        ],
        default="asked",
    )
