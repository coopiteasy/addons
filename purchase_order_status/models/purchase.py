# -*- coding: utf-8 -*-
# © 2019 Houssine BAKKALI, Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
from openerp.tools.float_utils import float_compare


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('state', 'order_line.qty_invoiced', 'order_line.product_qty')
    def _get_invoiced(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure') #noqa
        for po in self:
            invoice_status = 'no'
            if po.state in ['purchase', 'done']:
                if any(float_compare(line.qty_invoiced, line.product_qty, precision_digits=precision) == -1 for line in po.order_line): #noqa
                    invoice_status = 'to invoice'
                elif all(float_compare(line.qty_invoiced, line.product_qty, precision_digits=precision) >= 0 for line in po.order_line): #noqa
                    invoice_status = 'invoiced'
                else:
                    invoice_status = 'no'
            if invoice_status == 'invoiced':
                invoices = po.invoice_ids.filtered(
                            lambda inv: inv.state in ['open', 'paid', 'draft'])
                paid_invoices = po.invoice_ids.filtered(
                            lambda inv: inv.state == 'paid')
                if len(paid_invoices) == len(invoices):
                    invoice_status = 'paid'
            po.invoice_status = invoice_status

    @api.multi
    def _compute_delivery_info(self):
        for purchase_order in self:
            if purchase_order.state in ['sale', 'done']:
                done_date = None
                delivery_status = None
                for picking in purchase_order.picking_ids.sorted(
                        key=lambda r: r.name):
                    if picking.state == 'done':
                        if delivery_status != 'to_deliver':
                            if picking.date_done > done_date:
                                done_date = picking.date_done
                                delivery_status = 'delivered'
                    elif picking.state == 'cancel':
                        if not delivery_status:
                            done_date = None
                            delivery_status = 'cancelled'
                    else:
                        done_date = None
                        delivery_status = 'to_deliver'

                purchase_order.delivery_done_date = done_date
                purchase_order.delivery_status = delivery_status

    def _search_delivery_status(self, operator, value):
        filter_function = {
            '=': lambda po: po.delivery_status == value,
            '!=': lambda po: po.delivery_status != value,
        }
        purchase_orders = self.search([]).filtered(
            filter_function[operator]
        )
        return [('id', 'in', purchase_orders.ids)]

    delivery_done_date = fields.Datetime(
        compute='_compute_delivery_info',
        string="Delivery done date",
        readonly=True)

    delivery_status = fields.Selection(
        [('to_deliver', 'To deliver'),
         ('delivered', 'Delivered'),
         ('cancelled', 'Cancelled')],
        compute='_compute_delivery_info',
        string="Delivery status",
        search='_search_delivery_status',
        readonly=True)
    invoice_status = fields.Selection(selection_add=[
                        ('paid', 'Paid')],
                        compute='_get_invoiced',)
