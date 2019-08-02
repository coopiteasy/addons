# -*- coding: utf-8 -*-

from openerp import api, fields, models


class StockRecomputeAfterMove(models.TransientModel):
    _name = "stock.recompute.after.move"

    update = fields.Boolean(string="Update")
    print_log = fields.Boolean(string="Print computing in the log")

    @api.multi
    def recompute(self):
        self.ensure_one()
        stock_move_obj = self.env['stock.move']
        product_obj = self.env['product.product']

        products = product_obj.search([
                            ('finished_product', '=', True)
                            ])
        for product in products:
            moves = stock_move_obj.search([
                                ('state', '=', 'done'),
                                ('product_id', '=', product.id)
                               ], order="date asc")
            qty_after_move = 0
            if self.print_log:
                print ("========= product = " + product.name + " ==========")
            for move in moves:
                qty = 0
                if move.location_id.usage == 'customer' \
                        and move.location_dest_id.usage == 'internal':
                    qty = move.product_qty
                elif move.location_id.usage == 'transit' \
                        and move.location_dest_id.usage == 'internal':
                    qty = move.product_qty
                elif move.location_dest_id.usage == 'transit':
                    qty = -move.product_qty
                elif move.location_dest_id.usage in ['inventory',
                                                     'production',
                                                     'customer'
                                                     ]:
                    qty = -move.product_qty
                elif move.location_id.usage in ['inventory',
                                                'production',
                                                'internal'
                                                ]:
                    qty = move.product_qty

                qty_after_move += qty
                if self.print_log:
                    print ("move " + str(move.origin) +
                           " from " + move.location_id.name +
                           " to " + move.location_dest_id.name +
                           " on " + str(move.date) +
                           " moved qty is " + str(qty) + " qty after move "
                           "is " + str(move.quantity_after_move) +
                           " instead of " + str(qty_after_move))
                if self.update:
                    move.quantity_after_move = qty_after_move
        return True
