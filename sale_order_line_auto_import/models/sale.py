# -*- coding: utf-8 -*-
# © 2016 Houssine BAKKALI, Open Architects Consulting SPRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

from openerp import api, fields, models, SUPERUSER_ID
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

UNIT = dp.get_precision('Product Unit of Measure')


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    autoload_all_products = fields.Boolean(string="Auto-load all products")
    
#     @api.multi
#     @api.onchange('autoload_all_products')
#     def onchange_autoload(self):
#         if self.autoload_all_products:
#             if not self.partner_id:
#                 raise UserError(_('Please select a partner before ticking the checkbox'))
#  
#             else:
#                 self.order_line = self.create_order_line()
#                 return {}
        
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):    
        super(SaleOrder, self).onchange_partner_id()
        #self.env.cr.commit()
        self.order_line = self.create_order_line()
    
    @api.model
    def create_order_line(self):
        res = []
        if self.autoload_all_products:
            fpos = self.fiscal_position_id or self.partner_id.property_account_position_id
            for product in self.env['product.template'].search([('active','=',True),('sale_ok','=',True)]):
                values = {}
                values['order_id'] = self.id
                values['product_id'] = product.product_variant_ids.id
                values['product_uom'] = product.uom_id.id
                values['product_uom_qty'] = 1.0
                
                product_res = product.with_context(
                    lang=self.partner_id.lang,
                    partner=self.partner_id.id,
                    quantity= 1.0,
                    date=self.date_order,
                    pricelist=self.pricelist_id.id,
                    uom=product.uom_id.id
                )

                name = product_res.name_get()[0][1]
                if product_res.description_sale:
                    name += '\n' + product_res.description_sale
                values['name'] = name
        
                # If company_id is set, always filter taxes by the company
                taxes = product.taxes_id.filtered(lambda r: r.company_id.id == self.company_id.id)
                values['taxes_id'] = fpos.map_tax(taxes) if fpos else taxes
        
                if self.pricelist_id and self.partner_id:
                    values['price_unit'] = self.env['account.tax']._fix_tax_included_price(product_res.price, product_res.taxes_id, taxes)
                res.append(values)
        return res
