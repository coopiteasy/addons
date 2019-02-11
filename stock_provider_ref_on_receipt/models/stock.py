# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Product(models.Model):
    _inherit = 'stock.pack.operation'

    provider_ref = fields.Char(string="Provider Reference",
                               compute="_compute_product_code")

    @api.multi
    @api.depends('provider_ref')
    def _compute_product_code(self):
        product_supplier = self.env['product.supplierinfo'].search(
            [('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)])
        for line in self:
            line.provider_ref = product_supplier[0].product_code
