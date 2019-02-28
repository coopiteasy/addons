# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    provider_reference = fields.Char(string="Provider reference invoice",
                                     store=True)
