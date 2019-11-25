# -*- coding: utf-8 -*-
# © 201 Houssine BAKKALI (Coop IT Easy SCRLds)
import logging
from openerp import api, fields, models

_logger = logging.getLogger(__name__)


class StockRecomputeAfterMove(models.TransientModel):
    _name = "stock.recompute.after.move"

    update = fields.Boolean(string="Update")
    print_log = fields.Boolean(string="Print computing in the log")

    @api.multi
    def recompute(self):
        self.ensure_one()
        stock_move_obj = self.env["stock.move"]
        product_obj = self.env["product.product"]

        products = product_obj.search([("finished_product", "=", True)])
        for product in products:
            moves = stock_move_obj.search(
                [("state", "=", "done"), ("product_id", "=", product.id)],
                order="date asc",
            )
            qty_after_move = 0
            if self.print_log:
                _logger.info("======= product = " + product.name + " ========")
            for move in moves:
                qty = 0
                if (
                    move.location_id.usage == "customer"
                    and move.location_dest_id.usage == "internal"
                ):
                    qty = move.product_qty
                elif (
                    move.location_id.usage == "transit"
                    and move.location_dest_id.usage == "internal"
                ):
                    qty = move.product_qty
                elif move.location_dest_id.usage in [
                    "inventory",
                    "production",
                    "customer",
                    "transit",
                ]:
                    qty = -move.product_qty
                elif move.location_id.usage in [
                    "inventory",
                    "production",
                    "internal",
                ]:
                    qty = move.product_qty

                qty_after_move += qty

                if self.print_log:
                    _logger.info(
                        "move %s  from %s to %s on %s "
                        "moved qty is %s qty after move is %s "
                        "instead of %s",
                        move.origin,
                        move.location_id.name,
                        move.location_dest_id.name,
                        move.date,
                        qty,
                        move.quantity_after_move,
                        qty_after_move,
                    )

                if self.update:
                    move.quantity_after_move = qty_after_move
        return True
