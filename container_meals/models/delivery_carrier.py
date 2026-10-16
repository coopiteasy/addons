# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    # these methods are only used by delivery carriers with delivery_type
    # "base_on_rules".

    def _get_price_available(self, order):
        # this method computes the total price, quantity, weight and volume,
        # and calls _get_price_from_picking(). we need to pass the
        # container_cost for that method to be able to recompute the price
        # without the containers. we don't just remove the containers before
        # and after, because they should be taken into account to compute the
        # weight and the volume used when evaluating the rules.
        return super(
            DeliveryCarrier,
            self.with_context(container_cost=order._get_container_cost()),
        )._get_price_available(order)

    def _get_price_from_picking(self, total, weight, volume, quantity):
        # here the total contains the price of the containers, and the parent
        # method checks whether the amount exceeds free_over, so we need to
        # remove the container prices from it.
        container_cost = self.env.context.get("container_cost")
        return super()._get_price_from_picking(
            total - container_cost, weight, volume, quantity
        )
