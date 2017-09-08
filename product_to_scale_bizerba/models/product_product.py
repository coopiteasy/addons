# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp.osv import fields
from openerp.osv.orm import Model
import openerp.addons.decimal_precision as dp


class product_product(Model):
    _inherit = 'product.product'

    # Column Section
    _columns = {
        'scale_group_id': fields.many2one(
            'product.scale.group', string='Scale Group'),
        'scale_sequence': fields.integer(
            string='Scale Sequence'),
        'scale_tare_weight': fields.float(
            digits_compute=dp.get_precision('Stock Weight'),
            string='Scale Tare Weight',  help="Set here Constant tare weight"
            " for the given product. This tare will be substracted when"
            " the product is weighted. Usefull only for weightable product.\n"
            "The tare is defined with kg uom."),
    }

