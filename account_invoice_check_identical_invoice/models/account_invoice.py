# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import datetime as dt


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    identical_invoice_confirmed = fields.Boolean('Confirm Identical Invoice?',
                                                 default=False,
                                                 copy=False,
                                                 help="You need to check this box to validate the invoice if"
                                                      " invoices with the same partner,"
                                                      " invoice date and totam alount already exist.")
    identical_invoice_detected = fields.Boolean('identical_invoice_detected',
                                                compute='_check_identical_invoice')

    @api.onchange('partner_id', 'date_invoice')
    @api.multi
    def _onchange_check_identical_invoice(self):
        self._check_identical_invoice()

    @api.multi
    def _check_identical_invoice(self):
        for invoice in self:
            Invoice = self.env['account.invoice']
            duplicate_domain = [
                ('state', 'not in', ['draft', 'cancel']),
                ('partner_id.supplier', '=', True),
                ('partner_id', '=', invoice.partner_id.id),
            ]
            partner_invoices = Invoice.search(duplicate_domain)

            def equal_amount(i):
                return round(i.amount_total, 2) == round(invoice.amount_total, 2)

            def same_date(i):
                return i.date_invoice == invoice.date_invoice

            def invoiced_today(i):
                return i.date_invoice == str(dt.date.today()) and not invoice.date_invoice

            duplicate_invoices = partner_invoices.filtered(
                lambda i: equal_amount(i) and (same_date(i) or invoiced_today(i))
            )

            if duplicate_invoices:
                invoice.identical_invoice_detected = True
            else:
                invoice.identical_invoice_detected = False

    @api.multi
    def invoice_validate(self):
        self._check_identical_invoice()
        for invoice in self:
            if invoice.identical_invoice_detected and not invoice.identical_invoice_confirmed:
                raise ValidationError('We detected invoices with the same partner, date'
                                      ' and total. \n\nPlease check the' 
                                      ' "Confirm Identical Invoice?" box to continue')

        return super(AccountInvoice, self).invoice_validate()
