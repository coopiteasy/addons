# SPDX-FileCopyrightText: 2022 Coop IT Easy SCRLfs
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    is_customer_wallet_user = fields.Boolean(
        string="Is Customer Wallet User",
        compute="_compute_is_customer_wallet_user",
    )

    def _compute_is_customer_wallet_user(self):
        # TODO: Write a test for this.
        account_move_line = self.env["account.move.line"]
        for record in self:
            for partner in record.get_all_partners_in_family():
                if account_move_line.search(
                    [
                        ("partner_id", "=", partner.id),
                        ("account_id", "=", partner.customer_wallet_id.id),
                    ]
                ):
                    # FIXME: Optimise this. If `self` contains e.g. all
                    # partners, the above check is done once for every partner
                    # in the family, which is technically not necessary. But I'm
                    # not sure if we can just do
                    # `partner.is_customer_wallet_user = True` if partner is not
                    # in `self`.
                    record.is_customer_wallet_user = True
                    # Small optimisation to break early
                    break
            else:
                record.is_customer_wallet_user = False
