# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # fixme the module name is misleading, this field merely references
    #       the name of the invoice of the provider
    #       It is confusing with reference
    #       -> should be cleaned up during migration
    provider_reference = fields.Char(string="Provider reference invoice")
