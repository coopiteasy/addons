from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    provider_ref = fields.Char(string="Provider Reference",
                               compute="_compute_product_code")

    @api.multi
    @api.depends('provider_ref')
    def _compute_product_code(self):
        for product in self:
            product_supplier = self.env['product.supplierinfo'].search(
                [('product_tmpl_id', '=', product.product_id.product_tmpl_id.id)])
            if product_supplier:
                product.provider_ref = product_supplier[0].product_code
