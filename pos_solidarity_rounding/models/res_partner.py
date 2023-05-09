# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    enable_solidarity_rounding = fields.Boolean(
        "Solidarity Rounding",
        default=False,
        help="Round up payments at the Point of Sale to the nearest whole unit as a"
        " tip.",
    )
