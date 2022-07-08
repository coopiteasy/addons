# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    is_customer_wallet_user = fields.Boolean(
        string="Is Customer Wallet User",
    )
