# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.depends("partner_shipping_id", "order_line")
    def _compute_available_carrier(self):
        carriers = self.env["delivery.carrier"].search([])
        for so in self:
            products = list(so.order_line.mapped("product_id"))
            so.available_carrier_ids = carriers.available_carriers(
                so.partner_shipping_id, products
            )
