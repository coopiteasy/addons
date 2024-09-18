# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class EventTrackSpeakerTravelBooking(models.Model):
    _name = "event.track.speaker.travel.booking"
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

    ticket_ids = fields.Many2many("ir.attachment", string="Tickets")

    speaker_id = fields.Many2one("event.track.speaker", string="Speaker")

    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )
