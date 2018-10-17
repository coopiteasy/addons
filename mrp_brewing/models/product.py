# -*- coding: utf-8 -*-
# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models, _, SUPERUSER_ID


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    raw_material = fields.Boolean(
        string="Is raw material")
    finished_product = fields.Boolean(
        string="Is finished product")
    is_brewable = fields.Boolean(
        string="Is brewable")
    is_crate = fields.Boolean(
        string="Is Crate",
        default=False)
    brew_product_sequence = fields.Many2one(
        'ir.sequence',
        string="Brew product sequence")
    
    
class ProductPricelist(models.Model):
    _inherit = "product.pricelist"
    
    particular_conditions = fields.Text("Particular Conditions") 
