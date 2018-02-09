# -*- coding: utf-8 -*-
from datetime import datetime

from openerp import api, fields, models, _

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'sexy_invoice.report_sexy_invoice')