# -*- coding: utf-8 -*-
# © 2017 Houssine BAKKALI, Coop IT Easy
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp

class product_scale_group(models.Model):
    _inherit = 'product.scale.group'
    
    product_ids = fields.One2many('product.template', 'scale_group_id', string='Products')
    
    @api.multi
    def send_all_to_scale_create(self):
        for scale_group in self:
            scale_group.product_ids.filtered(lambda r: r.to_weight == True and r.sale_ok == True).send_scale_create()
            
    @api.multi
    def send_all_to_scale_write(self):
        for scale_group in self:
            scale_group.product_ids.filtered(lambda r: r.to_weight == True and r.sale_ok == True).send_scale_write()
    
    @api.multi
    def send_all_to_scale_unlink(self):
        for scale_group in self:
            scale_group.product_ids.send_scale_unlink()