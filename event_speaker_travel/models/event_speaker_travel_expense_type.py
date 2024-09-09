# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventSpeakerTravelExpenseType(models.Model):
    _name = "event.speaker.travel.expense.type"
    _description = "Speaker Travel Expense Type"

    name = fields.Char()
    price = fields.Float()
    description = fields.Text()
