# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import fields, models


class EventTrackDate(models.Model):
    _name = "event.track.date"
    _description = "Track dates"

    track_id = fields.Many2one("event.track")
    date = fields.Datetime()
