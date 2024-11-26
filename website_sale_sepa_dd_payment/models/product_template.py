# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "product.template"

    allow_sepa_dd_payment = fields.Boolean(string="Allow SEPA Direct Debit Payment")
