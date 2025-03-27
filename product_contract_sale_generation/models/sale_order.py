# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    created_from_contract = fields.Boolean(default=False, readonly=True)

    def action_create_contract(self):
        for order in self:
            if order.created_from_contract:
                return False
            else:
                return super().action_create_contract()
