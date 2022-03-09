# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def copy_qty(self):
        self.ensure_one()
        for move_without_package in self.move_ids_without_package:
            move_without_package.quantity_done = move_without_package.product_uom_qty
        return True
