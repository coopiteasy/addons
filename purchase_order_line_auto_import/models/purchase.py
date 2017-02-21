# -*- coding: utf-8 -*-
# � 2016 Houssine BAKKALI, Open Architects Consulting SPRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

from openerp import api, fields, models, SUPERUSER_ID
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

UNIT = dp.get_precision('Product Unit of Measure')


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        super(PurchaseOrder, self).onchange_partner_id()
        self.order_line = self.create_order_line()
        return {}
    
    @api.model
    def create_order_line(self):
        res = []
        fpos = self.fiscal_position_id
        for supplier_info in self.env['product.supplierinfo'].search([('name','=',self.partner_id.id)]):
            values = {}
            values['order_id'] = self.id
            values['product_id'] = supplier_info.product_tmpl_id.product_variant_ids.id
            values['product_qty'] = supplier_info.min_qty
            values['product_uom'] = supplier_info.product_uom.id
            values['price_unit'] = supplier_info.price
            values['name'] = supplier_info.product_tmpl_id.with_context({
                                'lang': self.partner_id.lang,
                                'partner_id': self.partner_id.id
                                }).display_name
            if self.date_order:
                values['date_planned'] = datetime.strptime(self.date_order, DEFAULT_SERVER_DATETIME_FORMAT) + relativedelta(days=supplier_info.delay if supplier_info else 0)
            else:
                values['date_planned'] = datetime.today() + relativedelta(days=supplier_info.delay if supplier_info else 0)
            if self.env.uid == SUPERUSER_ID:
                company_id = self.env.user.company_id.id
                values['taxes_id'] = fpos.map_tax(supplier_info.product_tmpl_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
            else:
                values['taxes_id'] = fpos.map_tax(supplier_info.product_tmpl_id.supplier_taxes_id)

            res.append(values)
        return res
