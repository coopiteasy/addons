# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        Invoice = self.env['account.invoice']
        for invoice in self:
            duplicate_domain = [
                ('state', 'not in', ['draft', 'cancel']),
                ('partner_id', '=', invoice.partner_id.id),
                ('date_invoice', '=', invoice.date_invoice),
            ]
            duplicate_invoices = Invoice.search(duplicate_domain)
            duplicate_invoices = duplicate_invoices.filtered(
                lambda i: round(i.amount_total, 2) == round(invoice.amount_total, 2)
            )
            if duplicate_invoices:
                raise ValidationError('Invoices %s have the same partner, date'
                                      ' and total, are you sure you want to'
                                      ' validate this invoice?'
                                      % duplicate_invoices.mapped('number'))

        return super(AccountInvoice, self).invoice_validate()
