# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Product(models.Model):
    _inherit = 'stock.pack.operation'

    display_weight = fields.Float('Weight', related='product_id.display_weight')
