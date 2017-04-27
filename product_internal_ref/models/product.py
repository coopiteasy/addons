# -*- coding: utf-8 -*-
# © 2017 Houssine BAKKALI - Coop IT Easy 
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    default_code = fields.Char(related='product_variant_ids.default_code', string='Internal Reference', store=True)