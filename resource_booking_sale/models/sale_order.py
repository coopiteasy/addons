# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    resource_booking_ids = fields.One2many(
        comodel_name="resource.booking",
        inverse_name="sale_order_id",
        string="Resource Booking",
    )

    def action_cancel(self):
        # TODO: Should we cancel resource_booking_ids here? The reverse is true.
        # If we implement this, we might get stuck in a recursive loop unless we
        # pass some context flags.
        return super().action_cancel()
