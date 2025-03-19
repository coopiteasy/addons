# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import fields, models


class EventTrackSession(models.Model):
    _inherit = "event.track"

    dates = fields.One2many(comodel_name="event.track.date", inverse_name="track_id")
