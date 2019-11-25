# -*- coding: utf-8 -*-
# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details. # noqa
# Copyright 2019 Coop IT Easy SCRLfs

from openerp import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    @api.depends("state")
    def get_on_hand(self):
        for move in self:
            if move.state == "done":
                move.quantity_after_move = move.product_id.qty_available

    lot_numbers = fields.Char(
        string="Lot Numbers",
        compute="_compute_lot_numbers",
        store=True,
        readonly=True,
    )
    quantity_after_move = fields.Integer(
        string="Quantity", compute="get_on_hand", store=True, readonly=True
    )
    brew_number = fields.Integer(string="Brew number", readonly=True)
    is_internal = fields.Boolean(
        string="Is Internal", compute="_compute_is_internal"
    )

    @api.multi
    @api.depends("quant_ids")
    def _compute_lot_numbers(self):

        for stock_move in self:
            lot_numbers = []
            for qid in stock_move.quant_ids:
                if (
                    qid.lot_id.display_name
                    and qid.lot_id.display_name not in lot_numbers
                ):
                    lot_numbers.append(qid.lot_id.display_name)
            stock_move.lot_numbers = "/".join(lot_numbers)

    @api.multi
    @api.depends("location_id", "location_dest_id")
    def _compute_is_internal(self):

        for move in self:
            move.is_internal = (
                move.location_id.usage == "internal"
                and move.location_dest_id.usage == "internal"
            )

    @api.model
    def _compute_product_domain(self, is_internal):
        if is_internal:
            domain = [
                ("type", "in", ["product", "consu"]),
                ("sale_ok", "=", True),
            ]
        else:
            domain = [("type", "in", ["product", "consu"])]

        return domain

    @api.onchange("is_internal")
    def onchange_is_internal(self):
        domain = self._compute_product_domain(self.is_internal)
        return {"value": [], "domain": {"product_id": domain}}

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super(StockMove, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu
        )
        if "fields" in result and "product_id" in result["fields"]:
            result["fields"]["product_id"][
                "domain"
            ] = self._compute_product_domain(
                result["fields"].get("is_internal", False)
            )
        return result


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(
        related="product_id.qty_available",
        string="Quantity On Hand",
        readonly=True,
    )


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    _order = "has_stock desc, create_date asc"

    qty_available = fields.Float(
        string="Quantity available",
        compute="_compute_qty_available",
        store=True,
    )

    has_stock = fields.Boolean(
        string="Has Stock", compute="_compute_qty_available", store=True
    )

    @api.multi
    @api.depends("quant_ids.reservation_id")
    def _compute_qty_available(self):
        for lot in self:
            quants = lot.quant_ids.filtered(
                lambda r: r.location_id.usage == "internal"
                and not r.reservation_id
            )  # noqa
            qty = sum(quants.mapped("qty"))
            lot.qty_available = qty
            lot.has_stock = qty > 0

    @api.model
    def _batch_compute_qty_available(self):
        lots = self.env["stock.production.lot"].search([])
        lots._compute_qty_available()


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date = fields.Datetime(
        "Creation Date",
        help="Creation Date, usually the time of the order",
        select=True,
        states={
            "done": [("readonly", False)],
            "cancel": [("readonly", False)],
        },
        track_visibility="onchange",
    )
    date_done = fields.Datetime(
        readonly=False, states={"done": [("readonly", True)]}
    )

    @api.multi
    def do_transfer(self):
        super(StockPicking, self).do_transfer()
        for picking in self:
            for move in picking.move_lines:
                move.date = picking.date_done
