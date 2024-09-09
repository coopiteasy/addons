# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventSpeakerTravelBooking(models.Model):
    _name = "event.speaker.travel.booking"
    _description = "Speaker Travel Booking"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    cost = fields.Float()

    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("payed", "Payed"),
            ("sent", "Sent"),
        ],
        default="draft",
    )

    speaker_id = fields.Many2one("event.track.speaker", string="Speaker")

    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )
