# -*- coding: utf-8 -*-
from openerp import api, fields, models


class MRPProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.model
    def _create_production_lot(self):
        mo_obj = self.env["mrp.production"]
        prod_lot_obj = self.env["stock.production.lot"]

        for prod_order in mo_obj.browse(self._context["active_id"]):
            prod_lot = prod_lot_obj.search(
                [
                    ("name", "=", prod_order.brew_order_name),
                    ("product_id", "=", prod_order.product_id.id),
                ]
            )
            if len(prod_lot) > 0:
                return prod_lot.id
            else:
                vals = {}
                vals["name"] = prod_order.brew_order_name
                vals["product_id"] = prod_order.product_id.id

                return prod_lot_obj.create(vals).id

    # Should only be visible when it is consume and produce mode
    lot_id = fields.Many2one(
        "stock.production.lot", "Lot", default=_create_production_lot
    )
