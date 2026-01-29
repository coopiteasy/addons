# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    is_customer_wallet_method = fields.Boolean(
        related="journal_id.is_customer_wallet_journal",
        store=True,
    )
