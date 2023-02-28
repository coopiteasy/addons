# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_enabled_customer_wallet = fields.Boolean(
        related="company_id.is_enabled_customer_wallet",
        string="Is Customer Wallet Enabled",
    )

    minimum_wallet_amount = fields.Monetary(
        string="Minimum Wallet amount",
        default=0.0,
        help="usually 0. You can enter a negative value,"
        " if you want to accept that the customer wallet"
        " is negative. Maybe useful if the sale amount"
        " is slightly higher than the wallet amount,"
        " to avoid charging the customer a small amount.",
    )
