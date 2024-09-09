# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventSpeakerTravelExpense(models.Model):
    _name = "event.speaker.travel.expense"
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
        "event.speaker.travel.expense.type", string="Type"
    )

    event_id = fields.Many2one(
        "event.event", related="speaker_id.event_id", string="Event", store="True"
    )

    @api.depends("expense_type_id.price")
    def _compute_cost(self):
        self.cost = self.expense_type_id.price * self.quantity
