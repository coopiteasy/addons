# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestDeliveryDistributionList(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.carrier_1 = cls._create_partner("carrier 1", carrier_delivery=True)
        cls.carrier_2 = cls._create_partner("carrier 2", carrier_delivery=True)
        cls.deposit_point_1 = cls._create_partner(
            "deposit point 1",
            quantity_to_deliver=42,
            deposit_point=True,
            carrier_id=cls.carrier_1.id,
        )
        cls.deposit_point_2 = cls._create_partner(
            "deposit point 2",
            quantity_to_deliver=6,
            deposit_point=True,
            carrier_id=cls.carrier_1.id,
        )
        cls.deposit_point_3 = cls._create_partner(
            "deposit point 3",
            quantity_to_deliver=32,
            deposit_point=True,
            carrier_id=cls.carrier_2.id,
        )
        # consumable product for most tests
        cls.product_1 = cls.env["product.product"].create({"name": "product 1"})
        # storable product for tests involving available quantities
        cls.product_2 = cls.env["product.product"].create(
            {
                "name": "product 2",
                "type": "product",
            }
        )
        cls.sale_journal = cls.env["account.journal"].search([("type", "=", "sale")])[0]

    @classmethod
    def _create_partner(
        cls,
        name,
        quantity_to_deliver=0,
        deposit_point=False,
        carrier_delivery=False,
        carrier_id=False,
    ):
        return cls.env["res.partner"].create(
            {
                "name": name,
                "quantity_to_deliver": quantity_to_deliver,
                "deposit_point": deposit_point,
                "carrier_delivery": carrier_delivery,
                "carrier_id": carrier_id,
            }
        )

    @classmethod
    def _create_delivery_distribution_list(cls):
        return cls.env["delivery.distribution.list"].create(
            {
                "distribution_date": datetime.date(2025, 4, 1),
                "product_id": cls.product_1.id,
                "journal_id": cls.sale_journal.id,
            }
        )

    @classmethod
    def _create_delivery_distribution_line(cls):
        distribution_list = cls._create_delivery_distribution_list()
        distribution_list.generate_distribution_list()
        return distribution_list.distribution_lines[0]

    @classmethod
    def _create_delivery_distribution_line_in_sale_state(cls):
        line = cls._create_delivery_distribution_line()
        line.generate_sale_order()
        return line

    def test_generate_distribution_list_empty(self):
        "Should create delivery distribution lines."
        distribution_list = self._create_delivery_distribution_list()
        self.assertFalse(distribution_list.distribution_lines)
        distribution_list.generate_distribution_list()
        lines = distribution_list.distribution_lines
        self.assertEqual(len(lines), 3)
        for line in lines:
            self.assertEqual(line.distribution_list_id, distribution_list)
            self.assertEqual(line.product_id, self.product_1)
        self.assertEqual(lines[0].partner_id, self.deposit_point_1)
        self.assertEqual(lines[0].carrier_id, self.carrier_1)
        self.assertEqual(lines[0].ordered_qty, 42)
        self.assertEqual(lines[0].delivered_qty, 42)
        self.assertEqual(lines[1].partner_id, self.deposit_point_2)
        self.assertEqual(lines[1].carrier_id, self.carrier_1)
        self.assertEqual(lines[1].ordered_qty, 6)
        self.assertEqual(lines[1].delivered_qty, 6)
        self.assertEqual(lines[2].partner_id, self.deposit_point_3)
        self.assertEqual(lines[2].carrier_id, self.carrier_2)
        self.assertEqual(lines[2].ordered_qty, 32)
        self.assertEqual(lines[2].delivered_qty, 32)

    def test_generate_distribution_list_existing(self):
        """
        Should delete existing delivery distribution lines and create new
        ones.
        """
        distribution_list = self._create_delivery_distribution_list()
        self.assertFalse(distribution_list.distribution_lines)
        distribution_list.generate_distribution_list()
        lines = distribution_list.distribution_lines
        self.assertEqual(len(lines), 3)
        distribution_list.generate_distribution_list()
        new_lines = distribution_list.distribution_lines
        self.assertEqual(len(new_lines), 3)
        self.assertNotEqual(new_lines, lines)
        for line in lines:
            self.assertFalse(line.exists())

    def test_generate_distribution_list_non_draft(self):
        "Should have no effect."
        distribution_list = self._create_delivery_distribution_list()
        self.assertFalse(distribution_list.distribution_lines)
        distribution_list.generate_distribution_list()
        lines = distribution_list.distribution_lines
        self.assertEqual(len(lines), 3)
        distribution_list.action_validate()
        distribution_list.generate_distribution_list()
        new_lines = distribution_list.distribution_lines
        self.assertEqual(new_lines, lines)

    def test_generate_distribution_list_set_name(self):
        "Should set the name of the distribution list."
        distribution_list = self._create_delivery_distribution_list()
        self.assertFalse(distribution_list.name)
        distribution_list.generate_distribution_list()
        self.assertTrue(distribution_list.name.startswith("DDL/"))

    def test_generate_distribution_list_keep_existing_name(self):
        "Should not set the name of the distribution list if already set."
        distribution_list = self._create_delivery_distribution_list()
        name = "test distribution list"
        distribution_list.name = name
        distribution_list.generate_distribution_list()
        self.assertEqual(distribution_list.name, name)

    def test_generate_distribution_list_ignore_zero_quantity(self):
        """
        Should not create delivery distribution lines for deposit points
        having a quantity_to_deliver at 0.
        """
        distribution_list = self._create_delivery_distribution_list()
        self.deposit_point_2.quantity_to_deliver = 0
        self.assertFalse(distribution_list.distribution_lines)
        distribution_list.generate_distribution_list()
        lines = distribution_list.distribution_lines
        self.assertEqual(len(lines), 2)

    def test_distribution_line_generate_sale_order(self):
        "Should create a sale order for the delivery distribution line."
        line = self._create_delivery_distribution_line()
        self.assertFalse(line.sale_order)
        line.generate_sale_order()
        sale_order = line.sale_order
        self.assertEqual(sale_order.partner_id, self.deposit_point_1)
        self.assertEqual(sale_order.distribution_list_id, line.distribution_list_id)
        self.assertEqual(sale_order.distribution_carrier_id, self.carrier_1)
        order_line = sale_order.order_line
        self.assertEqual(order_line.order_id, sale_order)
        self.assertEqual(order_line.product_id, self.product_1)
        self.assertEqual(order_line.product_uom_qty, 42)
        self.assertEqual(order_line.product_uom, self.product_1.uom_id)
        self.assertEqual(line.state, "sale")

    def test_distribution_line_invoice_sale_order(self):
        "Should create an invoice."
        line = self._create_delivery_distribution_line_in_sale_state()
        self.assertFalse(line.sale_order.invoice_ids)
        line.invoice_sale_order()
        self.assertTrue(line.sale_order.invoice_ids)
        self.assertEqual(line.sale_order.invoice_status, "invoiced")
        self.assertEqual(line.state, "invoiced")

    def test_distribution_line_invoice_sale_order_twice(self):
        "Should have no effect if run multiple times."
        line = self._create_delivery_distribution_line_in_sale_state()
        self.assertFalse(line.sale_order.invoice_ids)
        line.invoice_sale_order()
        invoice = line.sale_order.invoice_ids
        line.invoice_sale_order()
        self.assertEqual(line.sale_order.invoice_ids, invoice)
        self.assertEqual(line.sale_order.invoice_status, "invoiced")
        self.assertEqual(line.state, "invoiced")

    def test_distribution_line_invoice_sale_order_wrong_state(self):
        "Should have no effect if line not in sale or sale_sent state."
        line = self._create_delivery_distribution_line()
        state = line.state
        self.assertFalse(line.sale_order.invoice_ids)
        line.invoice_sale_order()
        self.assertFalse(line.sale_order.invoice_ids)
        self.assertEqual(line.state, state)

    def test_distribution_line_invoice_sale_order_validate_picking(self):
        "Should set the quantities on the stock picking and validate it."
        line = self._create_delivery_distribution_line_in_sale_state()
        line.invoice_sale_order()
        picking = line.sale_order.picking_ids
        self.assertTrue(len(picking), 1)
        move = picking.move_ids
        self.assertTrue(len(move), 1)
        move_line = move.move_line_ids
        self.assertTrue(len(move_line), 1)
        self.assertEqual(move_line.qty_done, 42)
        self.assertEqual(picking.state, "done")
        self.assertEqual(move.state, "done")
        self.assertEqual(move_line.state, "done")

    def test_distribution_line_invoice_sale_order_picking_origin(self):
        """
        Should ignore stock pickings that do not originate from the sale
        order.
        """
        line = self._create_delivery_distribution_line_in_sale_state()
        test_picking = self.env["stock.picking"].create(
            {
                "name": "test stock picking 1",
                "sale_id": line.sale_order.id,
                "origin": "dummy origin",
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
            }
        )
        line.invoice_sale_order()
        self.assertEqual(test_picking.state, "draft")
        self.assertEqual(line.state, "invoiced")

    def test_distribution_line_invoice_sale_order_picking_state(self):
        """
        Should ignore stock pickings in cancel or done state.
        """
        line = self._create_delivery_distribution_line_in_sale_state()
        picking = line.sale_order.picking_ids
        # change state of the move to change the one of the picking.
        picking.move_ids.state = "cancel"
        self.assertEqual(picking.state, "cancel")
        line.invoice_sale_order()
        self.assertEqual(picking.state, "cancel")

    def test_distribution_line_invoice_sale_order_picking_not_assigned(self):
        """
        Should ensure that the stock picking is in assigned state.
        """
        line = self._create_delivery_distribution_line_in_sale_state()
        picking = line.sale_order.picking_ids
        # change state of the move to change the one of the picking.
        picking.move_ids.state = "draft"
        self.assertEqual(picking.state, "draft")
        line.invoice_sale_order()
        self.assertEqual(picking.state, "done")

    def test_distribution_line_invoice_sale_order_not_enough_stock(self):
        """
        Should raise an error if there is not enough stock available.
        """
        distribution_list = self.env["delivery.distribution.list"].create(
            {
                "distribution_date": datetime.date(2025, 4, 1),
                # use storable product without any stock
                "product_id": self.product_2.id,
                "journal_id": self.sale_journal.id,
            }
        )
        distribution_list.generate_distribution_list()
        line = distribution_list.distribution_lines[0]
        line.generate_sale_order()
        with self.assertRaises(UserError):
            line.invoice_sale_order()

    def test_distribution_line_invoice_sale_order_picking_move_quantity(self):
        "Should update the done quantity of the stock picking moves."
        line = self._create_delivery_distribution_line_in_sale_state()
        move = line.sale_order.picking_ids.move_ids
        self.assertEqual(move.quantity_done, 0)
        line.invoice_sale_order()
        self.assertEqual(move.quantity_done, 42)
        self.assertEqual(move.product_uom_qty, 42)

    def test_distribution_line_invoice_sale_order_picking_move_sold_quantity(self):
        """
        Should update the quantity of the stock moves if the sold quantity is
        smaller than planned.
        """
        line = self._create_delivery_distribution_line_in_sale_state()
        move = line.sale_order.picking_ids.move_ids
        self.assertEqual(move.product_uom_qty, 42)
        line.sold_qty = 37
        line.invoice_sale_order()
        self.assertEqual(move.quantity_done, 37)
        self.assertEqual(move.product_uom_qty, 37)
        self.assertEqual(move.state, "done")

    def test_distribution_line_invoice_sale_order_picking_move_other_product(self):
        """
        Should not update the quantities of the stock moves related to a
        different product.
        """
        line = self._create_delivery_distribution_line_in_sale_state()
        move = line.sale_order.picking_ids.move_ids
        move.product_id = self.product_2
        line.invoice_sale_order()
        self.assertEqual(move.quantity_done, 0)
        self.assertEqual(move.state, "assigned")

    def test_distribution_line_invoice_sale_order_picking_cancel_backorder(self):
        """
        Should not create a backorder picking in case quantities don't
        match.
        """
        line = self._create_delivery_distribution_line_in_sale_state()
        picking = line.sale_order.picking_ids
        line.sold_qty = 37
        line.invoice_sale_order()
        backorder_picking = self.env["stock.picking"].search(
            [("backorder_id", "=", picking.id)]
        )
        self.assertFalse(backorder_picking)

    def test_distribution_line_invoice_sale_order_set_journal(self):
        """
        Should force the invoice journal to the one of the distribution list.
        """
        line = self._create_delivery_distribution_line_in_sale_state()
        test_journal = self.env["account.journal"].create(
            {
                "name": "test journal 1",
                "code": "test_journal_1",
                "type": "sale",
            }
        )
        line.distribution_list_id.journal_id = test_journal
        line.invoice_sale_order()
        self.assertEqual(line.sale_order.invoice_ids.journal_id, test_journal)
