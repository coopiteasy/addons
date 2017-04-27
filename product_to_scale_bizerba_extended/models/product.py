# -*- coding: utf-8 -*-
# © 2017 Houssine BAKKALI, Coop IT Easy
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class product_product(models.Model):
    _inherit = 'product.template'

    scale_group_id = fields.Many2one(related="product_variant_ids.scale_group_id", string='Scale Group', store=True)
    scale_sequence = fields.Integer(related="product_variant_ids.scale_sequence",string='Scale Sequence', store=True)
    scale_tare_weight = fields.Float(related="product_variant_ids.scale_tare_weight",string='Scale Tare Weight', store=True,
        help="Set here Constant tare weight"
        " for the given product. This tare will be substracted when"
        " the product is weighted. Usefull only for weightable product.\n"
        "The tare is defined with kg uom.")
