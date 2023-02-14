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
    sale_order_amount_tax = fields.Monetary(
        related="sale_order_id.amount_tax",
        currency_field="sale_order_currency_id",
        readonly=True,
    )
    sale_order_amount_total = fields.Monetary(
        related="sale_order_id.amount_total",
        currency_field="sale_order_currency_id",
        readonly=True,
    )
    sale_order_amount_untaxed = fields.Monetary(
        related="sale_order_id.amount_untaxed",
        currency_field="sale_order_currency_id",
        readonly=True,
    )
    sale_order_line_ids = fields.One2many(
        related="sale_order_id.order_line",
        readonly=False,
    )
    sale_order_company_id = fields.Many2one(
        related="sale_order_id.company_id",
        readonly=True,
    )
    sale_order_currency_id = fields.Many2one(
        related="sale_order_id.currency_id",
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
    sale_order_state = fields.Selection(
        related="sale_order_id.state",
        string="Sales Order State",
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
            self.env["sale.order"].create(
                {
                    "partner_id": booking_id.partner_id.id,
                    "resource_booking_ids": [booking_id.id],
                }
            )
            booking_id.sync_sale_order_lines()
        return booking_id

    def write(self, vals):
        super().write(vals)
        if vals.get("combination_id"):
            self.sync_sale_order_lines()

    def toggle_active(self):
        super().toggle_active()
        for booking in self:
            # If the booking becomes active again, re-set the sale order's state
            # to draft.
            if booking.active:
                booking.sale_order_id.action_draft()

    def action_cancel(self):
        for booking in self:
            booking.sale_order_id.action_cancel()
        return super().action_cancel()

    def action_sale_order_confirm(self):
        for booking in self:
            booking.sale_order_id.action_confirm()
        return True

    def action_sale_order_quotation_send(self):
        self.ensure_one()
        return self.sale_order_id.action_quotation_send()

    def sync_sale_order_lines(self):
        for booking in self:
            booking_line = booking.sale_order_line_ids.filtered(
                lambda line: line.product_id == booking.product_id
            )
            if not booking_line:
                self.env["sale.order.line"].create(
                    {
                        # TODO: Verify this.
                        "name": _("Booking for %s") % booking.partner_id.name,
                        "sequence": 1,
                        "product_id": booking.product_id.id,
                        "order_id": booking.sale_order_id.id,
                    }
                )
            booking_resources = booking.combination_id.resource_ids
            order_line_resource_map = {
                line.product_id.resource_ids: line
                for line in booking.sale_order_line_ids
            }
            order_line_resources = self.env["resource.resource"].union(
                *order_line_resource_map.keys()
            )
            # Add missing sale order lines.
            for resource in booking_resources - order_line_resources:
                self.env["sale.order.line"].create(
                    {
                        "product_id": resource.product_id.id,
                        "order_id": booking.sale_order_id.id,
                    }
                )
            # Remove superfluous sale order lines.
            for resource in order_line_resources - booking_resources:
                try:
                    order_line_resource_map[resource].unlink()
                except KeyError:
                    pass
