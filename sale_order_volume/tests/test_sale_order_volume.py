# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import unittest

from odoo.tests import TransactionCase


class SaleOrderVolumeCase(TransactionCase):
    @unittest.expectedFailure
    def test_sale_order_volumes(self):
        sale_order = self.browse_ref("sale.sale_order_4")
        product = self.browse_ref("product.product_delivery_01")
        service_cat = self.browse_ref("product.product_category_3")
        office_furniture_cat = self.browse_ref("product.product_category_5")

        # trigger
        order_line = sale_order.order_line.filtered(lambda ol: ol.product_id == product)
        order_line.product_uom_qty = 3

        # assert
        service_volume = sale_order.volume_per_category.filtered(
            lambda vpc: vpc.category_id == service_cat
        )
        office_furniture_volume = sale_order.volume_per_category.filtered(
            lambda vpc: vpc.category_id == office_furniture_cat
        )

        self.assertEquals(service_volume.volume, 0)
        self.assertEquals(service_volume.pallet_count, 1)
        self.assertEquals(office_furniture_volume.volume, 15.6)
        # (15.6 (volume) // 1.75 (pallet volume)) + 1 = 9
        self.assertEquals(office_furniture_volume.pallet_count, 9)
