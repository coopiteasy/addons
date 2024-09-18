# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class EventSpeakerTravelExpenseType(models.Model):
    _name = "event.track.speaker.travel.expense.type"
    _description = "Speaker Travel Expense Type"

    name = fields.Char()
    price = fields.Float()
    description = fields.Text()
