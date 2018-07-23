# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    identical_invoice_confirmed = fields.Boolean('Confirm Identical Invoice?',
                                                 default=False,
                                                 help="HELP!!!")
    identical_invoice_detected = fields.Boolean('identical_invoice_detected',
                                                compute='_check_identical_invoice')

    @api.multi
    def _check_identical_invoice(self):
        for invoice in self:
            Invoice = self.env['account.invoice']
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
                self.identical_invoice_detected = True
            else:
                self.identical_invoice_detected = False


    @api.multi
    def invoice_validate(self):
        for invoice in self:
            if invoice.identical_invoice_detected and not invoice.identical_invoice_confirmed:
                raise ValidationError('We detected invoices with the same partner, date'
                                      ' and total. Please check the' 
                                      'Confirm Identical Invoice? box to continue')

        return super(AccountInvoice, self).invoice_validate()
