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

    def available_carriers(self, partner, products=None):
        """
        Overwrite the `available_carriers` function in the
        delivery.carrier in the delivery module.

        Returns a recordset of the available delivery carrier given the
        partner location and the authorised carrier for the products.
        """
        delivery_carriers = self
        if partner:
            delivery_carriers = delivery_carriers.filtered(
                lambda c: c._match_address(partner)
            )
        if products:
            delivery_carriers = delivery_carriers.filtered(
                lambda c: c._can_be_used_to_deliver_products(products)
            )
        return delivery_carriers
