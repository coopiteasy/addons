# -*- coding: utf-8 -*-

import werkzeug

from openerp import models, fields, api
from openerp.addons.web.http import request

class WebSite(models.Model):
    _inherit = "website"
      
     
    def is_product_in_cart(self, product_id):
        if isinstance(product_id, (list, tuple)):
            product_id = product_id[0]
        ses_order_recs = request.website.sale_get_order(force_create=1)
        product_uom_qty= 0.0
        if ses_order_recs:
            so_line_obj = self.env['sale.order.line']
            so_line_ids = so_line_obj.sudo().search([('order_id', '=', ses_order_recs.id), ('product_id', '=', product_id)])
            for so_line in so_line_ids:
                product_uom_qty += so_line.product_uom_qty
            return int(product_uom_qty)
        return int(product_uom_qty)

