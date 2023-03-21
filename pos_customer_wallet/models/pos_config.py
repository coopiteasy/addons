# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_enabled_customer_wallet = fields.Boolean(
        related="company_id.is_enabled_customer_wallet",
        string="Is Customer Wallet Enabled",
    )

    minimum_wallet_amount = fields.Monetary(
        string="Minimum Wallet Amount",
        compute="_compute_minimum_wallet_amount",
    )

    @api.depends(
        "journal_ids.is_customer_wallet_journal",
        "journal_ids.minimum_wallet_amount",
    )
    def _compute_minimum_wallet_amount(self):
        for config in self:
            config.minimum_wallet_amount = min(
                config.mapped("journal_ids.minimum_wallet_amount")
            )
