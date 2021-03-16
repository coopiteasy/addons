from odoo import models, api, _
from odoo.exceptions import UserError


class AccountInvoiceConfirm(models.TransientModel):
    """
    This wizard will confirm and send all the selected draft invoices
    """

    _name = "account.invoice.validate.send"
    _description = "Confirm and send the selected invoices"

    @api.multi
    def invoice_validate_send(self):
        active_ids = self.env.context.get('active_ids', []) or []

        template_ref = "account.email_template_edi_invoice"
        mail_template = self.env.ref(template_ref)

        for invoice in self.env['account.invoice'].browse(active_ids):
            if invoice.state != 'draft':
                raise UserError(_("Selected invoice(s) cannot be confirmed as "
                                  "they are not in 'Draft' state."))
            invoice.action_invoice_open()
            mail_template.send_mail(invoice.id, False)
        return {'type': 'ir.actions.act_window_close'}
