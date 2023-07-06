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
        "payment_method_ids.journal_id.is_customer_wallet_journal",
        "payment_method_ids.journal_id.minimum_wallet_amount",
    )
    def _compute_minimum_wallet_amount(self):
        for config in self:
            wallet_method = config.payment_method_ids.filtered(
                lambda method: method.journal_id.is_customer_wallet_journal
            )
            if wallet_method:
                config.minimum_wallet_amount = min(
                    wallet_method.mapped("journal_id.minimum_wallet_amount")
                )
            else:
                config.minimum_wallet_amount = False
