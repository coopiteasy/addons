# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Product(models.Model):
    _inherit = 'stock.pack.operation'

    # weight = fields.Float('Weight', related='product_id.weight')
    display_weight = fields.Float(string="Display weight",
                                  compute="_compute_weight")
    # display_unit = fields.Float(string="Display unit")

    @api.multi
    # @api.depends('display_weight', 'display_unit')
    @api.depends('display_weight')
    def _compute_weight(self):
        for line in self:
            line.display_weight = line.product_id.display_weight
            # line.display_unit = line.product_id.display_unit
