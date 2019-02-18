# -*- coding: utf-8 -*-
from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_done(self):
        super(StockPicking, self).action_done()
        picking_mail_template = self.env.ref(
            'delivery.mail_template_data_delivery_confirmation',
            False
            )
        invoice_mail_template = self.env.ref(
            'account.email_template_edi_invoice',
            False)
        for picking in self:
            sale_order = picking.sale_id
            if sale_order.invoice_status == 'to invoice':
                invoice_ids = sale_order.action_invoice_create()

                for invoice in self.env['account.invoice'].browse(invoice_ids):
                    invoice.action_invoice_open()
                    # sale_order.invoice_ids.journal_id = journal_id
                    if picking.carrier_id.auto_send_invoice:
                        invoice_mail_template.send_mail(invoice.id)
            if picking.carrier_id.auto_send_picking:
                picking_mail_template.send_mail(picking.id)
