# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class EventTrackSpeakerBookProvider(models.Model):
    _name = "event.track.speaker.book.provider"
    _description = "Track Speaker Book Provider"

    name = fields.Char()
