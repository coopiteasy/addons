# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        # TODO: Verify this.
        required=True,
    )

    sale_order_line_id = fields.Many2one(
        "sale.order.line",
        string="Sale Order Line",
        copy=False,
        index=True,
        # TODO: Determine what to do here.
        # ondelete="cascade",
        track_visibility="onchange",
    )
    sale_order_id = fields.Many2one(
        related="sale_order_line_id.order_id",
        string="Sale Order",
        readonly=True,
    )

    @api.model
    def create(self, vals):
        # FIXME: I think it would be nicer to do this with magic numbers, but I
        # couldn't get that to work.
        booking_id = super().create(vals)
        if not booking_id.sale_order_line_id:
            order_id = self.env["sale.order"].create(
                {
                    "partner_id": booking_id.partner_id.id,
                }
            )
            line_id = self.env["sale.order.line"].create(
                {
                    # TODO: Verify this.
                    "name": _("Booking for %s") % booking_id.partner_id.name,
                    "sequence": 1,
                    "product_id": booking_id.product_id.id,
                    "order_id": order_id.id,
                    "resource_booking_ids": [booking_id.id],
                }
            )
        return booking_id
