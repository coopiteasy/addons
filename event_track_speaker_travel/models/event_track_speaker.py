# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class EventTrackSpeaker(models.Model):
    _inherit = "event.track.speaker"

    travel_booking_ids = fields.One2many(
        comodel_name="event.track.speaker.travel.booking", inverse_name="speaker_id"
    )
    travel_expense_ids = fields.One2many(
        comodel_name="event.track.speaker.travel.expense", inverse_name="speaker_id"
    )
    need_travel = fields.Boolean()
    has_travel = fields.Boolean(compute="_compute_has_travel")
    travel_cost = fields.Float(compute="_compute_travel_cost")

    @api.depends("travel_booking_ids.cost", "travel_expense_ids.cost")
    def _compute_travel_cost(self):
        for speaker in self:
            speaker.travel_cost = 0
            for booking in speaker.travel_booking_ids:
                if booking.status != "draft":
                    speaker.travel_cost += booking.cost
            for expense in speaker.travel_expense_ids:
                if expense.status != "draft":
                    speaker.travel_cost += expense.cost

    @api.depends("travel_booking_ids", "travel_expense_ids")
    def _compute_has_travel(self):
        for speaker in self:
            booking_ok = not speaker.travel_booking_ids
            for booking in speaker.travel_booking_ids:
                booking_ok = booking.status == "payed"

            expense_ok = not speaker.travel_expense_ids
            for expense in speaker.travel_expense_ids:
                expense_ok = expense.status != "draft"

            speaker.has_travel = booking_ok and expense_ok
