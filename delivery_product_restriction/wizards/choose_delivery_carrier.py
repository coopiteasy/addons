# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ChooseDeliveryCarrier(models.TransientModel):

    _inherit = "choose.delivery.carrier"

    @api.depends("partner_id", "order_id.order_line")
    def _compute_available_carrier(self):
        for rec in self:
            carriers = self.env["delivery.carrier"].search(
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", rec.order_id.company_id.id),
                ]
            )
            products = list(rec.order_id.order_line.mapped("product_id"))
            rec.available_carrier_ids = carriers.available_carriers(
                rec.order_id.partner_shipping_id, products
            )
