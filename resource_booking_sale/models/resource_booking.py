# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models
from odoo.tools.translate import _


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        # TODO: Verify this.
        required=True,
    )

    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sales Order",
        copy=False,
        readonly=True,
        track_visibility="onchange",
    )
    sale_order_line_ids = fields.One2many(
        related="sale_order_id.order_line",
    )
    sale_order_state = fields.Selection(
        related="sale_order_id.state",
        string="Sales Order State",
        readonly=True,
    )
    sale_order_company_id = fields.Many2one(
        related="sale_order_id.company_id",
        readonly=True,
    )
    sale_order_partner_id = fields.Many2one(
        related="sale_order_id.partner_id",
        readonly=True,
    )
    sale_order_pricelist_id = fields.Many2one(
        related="sale_order_id.pricelist_id",
        readonly=True,
    )

    @api.onchange("type_id")
    def _onchange_type_id(self):
        default_product_id = self.type_id.default_product_id
        if default_product_id:
            self.product_id = default_product_id

    @api.model
    def create(self, vals):
        # FIXME: I think it would be nicer to do this with magic numbers, but I
        # couldn't get that to work.
        booking_id = super().create(vals)
        if not booking_id.sale_order_id:
            order_id = self.env["sale.order"].create(
                {
                    "partner_id": booking_id.partner_id.id,
                    "resource_booking_ids": [booking_id.id],
                }
            )
            self.env["sale.order.line"].create(
                {
                    # TODO: Verify this.
                    "name": _("Booking for %s") % booking_id.partner_id.name,
                    "sequence": 1,
                    "product_id": booking_id.product_id.id,
                    "order_id": order_id.id,
                }
            )
        return booking_id

    def action_sale_order_confirm(self):
        for booking in self:
            booking.sale_order_id.action_confirm()
