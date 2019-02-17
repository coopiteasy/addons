# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Product(models.Model):
    _inherit = 'stock.pack.operation'

    weight = fields.Float('Weight', related='product_id.weight')
