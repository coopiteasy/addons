# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def copy_qty(self):
        self.ensure_one()
        for pack_operation in self.pack_operation_product_ids:
            pack_operation.qty_done = pack_operation.product_qty
        return True
