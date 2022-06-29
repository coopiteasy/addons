# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MrpUnbuild(models.Model):

    _inherit = "mrp.unbuild"

    @api.onchange("mo_id")
    def onchange_mo_id(self):
        # save and restore product_qty, which is set in super().
        current_product_qty = self.product_qty
        super().onchange_mo_id()
        self.product_qty = current_product_qty

    @api.onchange("product_id")
    def onchange_product_id(self):
        # reset fields linked to another product
        if self.mo_id.product_id != self.product_id:
            self.mo_id = False
        if self.lot_id.product_id != self.product_id:
            self.lot_id = False
        # bom_id will be set in super()
        self.bom_id = False
        super().onchange_product_id()
        if self.product_id:
            return {
                "domain": {
                    "mo_id": [
                        ("product_id", "=", self.product_id.id),
                        ("state", "=", "done"),
                    ]
                }
            }
        return {"domain": {"mo_id": [("state", "=", "done")]}}
