from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    provider_ref = fields.Char(
        string="Provider Reference", compute="_compute_product_code"
    )

    @api.multi
    def _compute_product_code(self):
        for move in self:
            product_supplier = self.env["product.supplierinfo"].search(
                [
                    (
                        "product_tmpl_id",
                        "=",
                        move.product_id.product_tmpl_id.id,
                    )
                ]
            )
            if product_supplier:
                move.provider_ref = product_supplier[0].product_code