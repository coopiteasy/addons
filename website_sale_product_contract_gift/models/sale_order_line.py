# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    gift_contract_id = fields.Many2one(
        comodel_name="contract.contract", string="Gift Contract", copy=False
    )
