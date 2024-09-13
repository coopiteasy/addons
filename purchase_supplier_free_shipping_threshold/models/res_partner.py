# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    free_shipping_threshold = fields.Monetary()
