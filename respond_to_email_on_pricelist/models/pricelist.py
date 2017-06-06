# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class ProductPricelist(models.Model):
    
    _inherit = 'product.pricelist'

    respond_to_email_address = fields.Char(string="Respond to")