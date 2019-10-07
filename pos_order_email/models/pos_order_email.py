from odoo import models, fields, api, _


# TODO: make this work
# from odoo.addons.point_of_sale.report import pos_receipt
# 
# class order_tva_included(pos_receipt.order):
# 
#     def __init__(self, cr, uid, name, context):
#         super(order_tva_included, self).__init__(cr, uid, name, context=context)
#         self.env = api.Environment(cr, uid, context)
# 
#     def netamount(self, order_line_id):
#         order_line = self.env['pos.order.line'].browse(order_line_id)
#         if order_line.order_id.config_id.iface_tax_included:
#             return order_line.price_subtotal_incl
#         else:
#             return order_line.price_subtotal
# 
# 
# class report_order_receipt(models.AbstractModel):
#     _inherit = 'report.point_of_sale.report_receipt'
#     _template = 'point_of_sale.report_receipt'
#     _wrapped_report_class = order_tva_included