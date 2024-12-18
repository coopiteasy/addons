# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("sepa_dd", "SEPA Direct Debit")],
        ondelete={"sepa_dd": "set default"},
    )
    sepa_dd_terms = fields.Html(string="SEPA Direct Debit Terms", translate=True)

    @api.depends("code")
    def _compute_view_configuration_fields(self):
        """Override of payment to hide the credentials page."""
        result = super()._compute_view_configuration_fields()
        self.filtered(lambda p: p.code == "sepa_dd").update(
            {
                "show_credentials_page": False,
                "show_payment_icon_ids": False,
                "show_pre_msg": False,
                "show_done_msg": False,
                "show_cancel_msg": False,
            }
        )
        return result
