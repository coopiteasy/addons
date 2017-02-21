# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    commitment_date = fields.Date(string='Commitment Date',
            help="Date by which the products are sure to be delivered. This is "
                 "a date that you can promise to the customer, based on the "
                 "Product Lead Times.")