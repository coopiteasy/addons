# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class DeliveryCarrier(models.Model):

    _inherit = "delivery.carrier"

    def _can_be_used_to_deliver_products(self, products):
        self.ensure_one()
        return all(
            not product.restrict_delivery_carrier_to
            or self in product.restrict_delivery_carrier_to
            for product in products
        )

    def _can_be_used_to_deliver_order_products(self, order):
        products = list(order.order_line.mapped("product_id"))
        return self._can_be_used_to_deliver_products(products)
