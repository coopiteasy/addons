# -*- coding: utf-8 -*-
from openerp import api, models


class ValidateSubscriptionRequest(models.TransientModel):
    _name = "invoice.batch.cancellation"

    @api.multi
    def do_cancellation(self):
        selected_invoices = self.env['account.invoice'].browse(
            self._context.get('active_ids'))
        invoices = selected_invoices.filtered(
            lambda record: record.state in ['open'])

        for invoice in invoices:
            invoice.signal_workflow('invoice_cancel')
        return True
