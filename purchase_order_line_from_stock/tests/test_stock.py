from odoo import tests


class TestStock(tests.common.TransactionCase):
    def test_order_line_from_stock(self):
        order = self.browse_ref("purchase.purchase_order_4")
        product = self.browse_ref("product.product_product_1")
        location_id = self.env.ref("stock.warehouse0").wh_output_stock_loc_id
        dest_loc = self.env.ref("stock.stock_location_customers")

        # Confirm order
        order.button_confirm()
        self.assertEquals(len(order.order_line), 3)
        self.assertEquals(len(order.picking_ids.move_ids_without_package), 3)

        # Add stock move to picking
        new_move = self.env["stock.move"].create(
            {
                "name": product.name,
                "product_id": product.id,
                "product_uom": product.uom_id.id,
                "quantity_done": 20,
                "location_id": location_id.id,
                "location_dest_id": dest_loc.id,
            }
        )
        order.picking_ids.move_ids_without_package = [(4, new_move.id, 0)]
        self.assertEquals(len(order.picking_ids.move_ids_without_package), 4)

        # Set one of the original stock moves to 'done':
        # At least one other element must have a quantity_done,
        # otherwise an action is returned notifying the user.
        order.picking_ids.move_ids_without_package[0].write(
            {"quantity_done": 1}
        )

        # Validate picking
        wizard = order.picking_ids.button_validate()
        backorder_confirmation = self.env[wizard["res_model"]].browse(
            wizard["res_id"]
        )
        backorder_confirmation.process_cancel_backorder()

        # Check that product is added to order
        self.assertEquals(len(order.order_line), 4)
        self.assertEquals(order.order_line[-1].qty_received, 20)
