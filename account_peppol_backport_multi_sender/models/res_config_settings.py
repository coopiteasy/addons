# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("account_peppol_eas", "account_peppol_endpoint")
    def _compute_smp_registration(self):
        # pylint: disable=missing-return
        super()._compute_smp_registration()
        # normally, if another company with the same peppol adress did already
        # register on the peppol network, account_peppol_smp_registration will
        # be False, but if the registration is not complete, we need to
        # prevent other companies to try to register as a receiver.
        company_sudo = self.sudo().env["res.company"]
        for config in self:
            if config.account_peppol_eas and config.account_peppol_endpoint:
                companies = company_sudo.search(
                    [
                        ("peppol_eas", "=", config.account_peppol_eas),
                        ("peppol_endpoint", "=", config.account_peppol_endpoint),
                        ("id", "!=", config.company_id.id),
                        (
                            "account_peppol_proxy_state",
                            "in",
                            ("smp_registration", "receiver"),
                        ),
                    ]
                )
                if companies:
                    config.account_peppol_smp_registration = False
