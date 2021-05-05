# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details. # noqa
# Copyright 2019 Coop IT Easy SCRLfs

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    lot_numbers = fields.Char(
        string="Lot Numbers",
        compute="_compute_lot_numbers",
        store=True,
        readonly=True,
    )
    quantity_after_move = fields.Integer(
        string="Quantity",
        compute="_compute_on_hand",
        store=True,
        readonly=True,
    )
    brew_number = fields.Integer(string="Brew number", readonly=True)
    is_internal = fields.Boolean(
        string="Is Internal", compute="_compute_is_internal"
    )

    @api.model
    @api.depends("state")
    def _compute_on_hand(self):
        for move in self:
            if move.state == "done":
                move.quantity_after_move = move.product_id.qty_available

    @api.multi
    @api.depends("move_line_ids.package_id.quant_ids")
    def _compute_lot_numbers(self):

        for stock_move in self:
            lot_numbers = []
            # for qid in stock_move.quant_ids:
            # package_id = Source Package ;
            # result_package_id = Destination Package
            for qid in stock_move.mapped("move_line_ids.package_id.quant_ids"):

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
