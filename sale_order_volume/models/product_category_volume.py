# © 2016 Robin Keunen, Coop IT Easy SCRL.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategoryVolume(models.Model):
    _name = "product.category.volume"
    _description = "Product Volume by Category"

    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    category_id = fields.Many2one(
        comodel_name="product.category", string="Product Category"
    )
    volume = fields.Float(string="Volume (m³)")
    pallet_count = fields.Integer(string="# Pallets")
