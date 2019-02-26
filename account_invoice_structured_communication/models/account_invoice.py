# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    partner_structured_communication = fields.Char(string="Partner Structured "
                                                          "Communication"
                                                   )

    @api.multi
    def _compute_ref(self):
        self.ensure_one()
        if not self.check_bbacomm('partner_structured_communication'):
            print("b is greater than a")
