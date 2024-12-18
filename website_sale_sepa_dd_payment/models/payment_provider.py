# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    custom_mode = fields.Selection(selection_add=[("sepa_dd", "SEPA Direct Debit")])
    sepa_dd_terms = fields.Html(string="SEPA Direct Debit Terms", translate=True)
