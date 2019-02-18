# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Product(models.Model):
    _inherit = 'stock.pack.operation'

    display_weight = fields.Float(string='Weight',
                                  related='product_id.display_weight')

    display_unit = fields.Many2one(
        'product.uom',
        'Weight Unit',
        related='product_id.display_unit'
    )
