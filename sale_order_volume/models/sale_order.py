# © 2016 Robin Keunen, Coop IT Easy SCRL.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from collections import defaultdict

from odoo import api, fields, models


def _compute_pallet_count(volume, pallet_volume):
    if not pallet_volume:
        return 0
    quotient, remainder = divmod(volume, pallet_volume)
    if remainder:
        return quotient + 1
    return quotient


class SaleOrder(models.Model):
    _inherit = "sale.order"

    volume = fields.Float(
        string="Order Volume (m³)", compute="_compute_order_volume", store=True
    )

    pallet_count = fields.Integer(
        string="Order # Pallets", compute="_compute_order_volume", store=True
    )

    volume_per_category = fields.One2many(
        comodel_name="product.category.volume",
        inverse_name="sale_order_id",
        string="Volume per Product Category",
    )

    @api.depends("order_line", "order_line.volume")
    def _compute_order_volume(self):

        for order in self:
            order_lines = order.order_line.filtered(
                lambda ol: ol.state not in ["cancel"]
            )

            order.volume = sum(ol.volume for ol in order_lines)
            order.pallet_count = _compute_pallet_count(
                order.volume, float(self.get_default_pallet_volume())
            )

    @api.model
    def get_default_pallet_volume(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_order_volume.pallet_volume")
            or 0
        )

    def compute_order_product_category_volumes(self):
        self.ensure_one()

        order_lines = self.order_line.filtered(lambda ol: ol.state not in ["cancel"])

        volume_per_category = defaultdict(float)
        for order_line in order_lines:
            category_id = order_line.product_id.categ_id.id
            volume_per_category[category_id] += order_line.volume

        existing_categories = {
            vpc.category_id.id: vpc for vpc in self.volume_per_category
        }

        for category_id, volume in volume_per_category.items():
            pallet_count = _compute_pallet_count(
                volume, float(self.get_default_pallet_volume())
            )
            # TODO: what if there is an existing category_id of which no
            # products are in the order anymore?
            if category_id in existing_categories:
                existing_categories[category_id].volume = volume
                existing_categories[category_id].pallet_count = pallet_count
            else:
                vals = {
                    "sale_order_id": self.id,
                    "category_id": category_id,
                    "volume": volume,
                    "pallet_count": pallet_count,
                }
                self.env["product.category.volume"].create(vals)

        return self.volume_per_category

    def compute_product_category_volumes(self):
        for order in self:
            order.compute_order_product_category_volumes()

    def write(self, values):
        ret = super(SaleOrder, self).write(values)
        self.compute_product_category_volumes()
        return ret
