# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_delivery_wizard(self):
        # remove the default delivery carrier if it cannot be used for this
        # sale order.
        action = super().action_open_delivery_wizard()
        carrier_id = action["context"]["default_carrier_id"]
        carrier = self.env["delivery.carrier"].browse(carrier_id)
        if not carrier._can_be_used_to_deliver_order_products(self):
            del action["context"]["default_carrier_id"]
        return action
