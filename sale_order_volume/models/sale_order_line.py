# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    volume = fields.Float(compute="_compute_volume", store=True)

    @api.depends("product_id.volume", "product_uom_qty")
    def _compute_volume(self):
        for line in self:
            line.volume = line.product_id.volume * line.product_uom_qty
