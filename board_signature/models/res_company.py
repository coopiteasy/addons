# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    board_representative = fields.Char(string="Board representative name")
    board_representative_function = fields.Char(string="Board representative function")
    board_representative_signature_scan = fields.Binary(
        string="Board representative signature"
    )
