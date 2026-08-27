# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class EventTrackSpeakerTravelExpense(models.Model):
    _name = "event.track.speaker.travel.expense"
    _description = "Speaker Travel Expense"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    cost = fields.Float(compute="_compute_cost", store=True)
    quantity = fields.Float()
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("payed", "Payed"),
        ],
        default="draft",
    )
    speaker_id = fields.Many2one("event.track.speaker", string="Speaker")
    expense_type_id = fields.Many2one(
        "event.track.speaker.travel.expense.type", string="Type"
    )

    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )

    @api.depends("quantity", "expense_type_id.price")
    def _compute_cost(self):
        for expense in self:
            expense.cost = expense.expense_type_id.price * expense.quantity
