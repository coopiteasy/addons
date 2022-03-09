from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    display_weight = fields.Float(string="Weight", related="product_id.display_weight")

    display_unit = fields.Many2one(
        "uom.uom", "Weight Unit", related="product_id.display_unit"
    )
