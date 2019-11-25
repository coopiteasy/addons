# -*- coding: utf-8 -*-
# Part of Open Architechts Consulting sprl. See LICENSE file for full
# copyright and licensing details.
from datetime import datetime, timedelta
from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _get_commitment_date(self):
        """Compute the commitment date"""
        for order in self:
            dates_list = []
            order_datetime = datetime.strptime(
                order.date_order, DEFAULT_SERVER_DATE_FORMAT
            )
            for line in order.order_line:
                if line.state == "cancel":
                    continue
                dt = order_datetime + timedelta(days=line.customer_lead or 0.0)
                dt_s = dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                dates_list.append(dt_s)
            if dates_list:
                return min(dates_list)

    delivery_done_date = fields.Datetime(
        compute="_compute_delivery_info",
        string="Delivery done date",
        readonly=True,
    )

    delivery_status = fields.Selection(
        [
            ("to_deliver", "To deliver"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_delivery_info",
        string="Delivery status",
        search="_search_delivery_status",
        readonly=True,
    )

    commitment_date = fields.Date(
        string="Commitment Date",
        default=_get_commitment_date,
        help="Date by which the products are sure to be delivered. This is a "
        "date that you can promise to the customer, based on the Product "
        "Lead Times.",
    )

    @api.multi
    def _compute_delivery_info(self):
        for sale_order in self:
            if sale_order.state in ["sale", "done"]:
                done_date = None
                delivery_status = None
                for picking in sale_order.picking_ids.sorted(
                    key=lambda r: r.name
                ):
                    if picking.state == "done":
                        if delivery_status != "to_deliver":
                            if picking.date_done > done_date:
                                done_date = picking.date_done
                                delivery_status = "delivered"
                    elif picking.state == "cancel":
                        if not delivery_status:
                            done_date = None
                            delivery_status = "cancelled"
                    else:
                        done_date = None
                        delivery_status = "to_deliver"

                sale_order.delivery_done_date = done_date
                sale_order.delivery_status = delivery_status

    def _search_delivery_status(self, operator, value):
        filter_function = {
            "=": lambda so: so.delivery_status == value,
            "!=": lambda so: so.delivery_status != value,
        }
        sale_orders = self.search([]).filtered(filter_function[operator])
        return [("id", "in", sale_orders.ids)]

    @api.multi
    @api.onchange("pricelist_id")
    def onchange_price_list(self):
        if not self.pricelist_id:
            self.note = ""
        else:
            self.note = self.pricelist_id.particular_conditions

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.onchange_price_list()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_lot_ids = fields.Many2many(
        "stock.production.lot",
        string="Stock Product Lot",
        compute="_compute_stock_product",
    )
    effective_date = fields.Date(
        related="order_id.effective_date", string="Effective Date"
    )

    @api.multi
    def _compute_stock_product(self):
        """Computes the delivered product lot on sale order lines, based on
        done stock moves related to its procurements
        """
        for line in self:
            product_lot_ids = []
            for move in line.procurement_ids.mapped("move_ids").filtered(
                lambda r: r.state == "done" and not r.scrapped
            ):
                if (
                    move.location_dest_id.usage == "customer"
                    and len(move.lot_ids) > 0
                ):
                    product_lot_ids.append(move.lot_ids.ids[0])
            line.product_lot_ids = product_lot_ids
