# Copyright 2020 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import TransactionCase


class SaleOrderVolumeCase(TransactionCase):
    def test_sale_order_volumes(self):
        sale_order = self.browse_ref("sale.sale_order_4")
        product = self.browse_ref("product.product_delivery_01")

        # trigger
        order_line = sale_order.order_line.filtered(lambda ol: ol.product_id == product)
        order_line.product_uom_qty = 3

        self.assertEqual(sale_order.volume, 15.6)
        # (15.6 (volume) // 1.75 (pallet volume)) + 1 = 9
        self.assertEqual(sale_order.pallet_count, 9)
