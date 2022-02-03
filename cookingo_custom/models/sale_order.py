# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import namedtuple

from odoo import api, fields, models

ContainerVolumes = namedtuple(
    "ContainerVolumes", ["container_1_volume", "container_2_volume"]
)
_EMPTY = ContainerVolumes(0, 0)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def calculate_volume_containers(self):
        """For every product template found in this sale order that
        is a meal, return a tuple
        (combined_container_1_volume, combined_container_2_volume).
        """
        templates = self.env["product.template"]
        result = dict()
        for line in self.order_line:
            product_id = line.product_id
            product_template = product_id.product_tmpl_id
            if product_id.is_meal:
                vols = result.setdefault(product_template, _EMPTY)
                result[product_template] = ContainerVolumes(
                    vols.container_1_volume + (product_id.container_1_volume * line.product_uom_qty),
                    vols.container_2_volume + (product_id.container_2_volume * line.product_uom_qty),
                )
        return result
