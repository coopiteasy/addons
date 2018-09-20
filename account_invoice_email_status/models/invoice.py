# -*- coding: utf-8 -*-


from openerp import api, fields, models


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    email_status = fields.Selection([
        ('outgoing', 'Outgoing'),
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('exception', 'Delivery Failed'),
        ('cancel', 'Cancelled'),
    ], 'Email Status', compute='compute_email_status')

    @api.multi
    def compute_email_status(self):
        for invoice in self:
            search_domain = [
                ('model', '=', 'account.invoice'),
                ('res_id', '=', invoice.id),
            ]
            sent_emails = (self.env['mail.mail']
                           .search(search_domain,
                                   order='date desc'))
            if len(sent_emails) > 0:
                last_sended_email = sent_emails[0]
                invoice.email_status = last_sended_email.state

    @api.model
    def do_not_auto_delete_mail_template(self):
        invoice_mail_template = (self.env['mail.template']
                                 .search([('model', '=', 'account.invoice')]))
        for mail_template in invoice_mail_template:
            mail_template.auto_delete = False
