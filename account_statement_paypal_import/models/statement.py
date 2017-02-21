# -*- coding: utf-8 -*-
###############################################################################
#
#   account_statement_paypal_import for Odoo
#   Copyright (C) 2012 Akretion Benoît GUILLOT <benoit.guillot@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import _, api, fields, models

#Paypal have localized content

BANK_TRANSFERS = [
    'Virement de fonds vers un compte bancaire',
    'T0400',
]

BANK_FEE = [
    u'Frais annulés',
]


# class AccountStatementProfil(orm.Model):
#     _inherit = "account.statement.profile"
# 
#     def get_import_type_selection(self, cr, uid, context=None):
#         """
#         Has to be inherited to add parser
#         """
#         res = super(AccountStatementProfil, self).get_import_type_selection(cr, uid, context=context)
#         res.extend([('paypal_csvparser', 'Parser for Paypal import statement'),
#                     ('daily_paypal_csvparser', 'Parser for daily Paypal import statement')
#             ])
#         return res


class account_bank_statement_line(models.Model):
    _inherit = "account.bank.statement.line"

    partner_name = fields.Char(string='Partner name')
    paypal_payment_type = fields.Char(string='Paypal Payment type')
    email_from = fields.Char(string='Email from')
    email_to = fields.Char(string='Email to')
    transaction_number = fields.Char(string='Transaction number')
    transaction_state = fields.Char(string='Transaction State')

# class AccountBankStatement(models.Model):
#     _inherit = "account.bank.statement"
# 
#     #TODO move in an other module
#     def get_account_for_counterpart(self, cr, uid,
#             amount, account_receivable, account_payable):
#         account_ids = self.pool['account.account'].\
#                 search(cr, uid, [['type', '=', 'view']])
#         return account_ids[0]

# class AccountStatementCompletionRule(models.Model):
#     _inherit = "account.statement.completion.rule"
# 
#     def get_functions(self, cr, uid, context=None):
#         res = super(AccountStatementCompletionRule, self).get_functions(cr, uid, context=context)
#         res.extend([('get_from_paypal_payment_type', 'From Paypal Payment Type'),
#                     ('get_from_paypal_transaction_state', 'From Paypal Transaction State'),
#                     ('get_from_paypal_partner_email', 'From Paypal Partner Email'),
#                    ])
#         return res
# 
#     def get_from_paypal_payment_type(self, cr, uid, line_id, context=None):
#         st_obj = self.pool['account.bank.statement.line']
#         st_line = st_obj.browse(cr, uid, line_id, context=context)
#         res = {}
#         if st_line.paypal_payment_type in BANK_TRANSFERS:
#             res['account_id'] = st_line.statement_id.profile_id.internal_account_transfer_id.id
#             res['partner_id'] = st_line.company_id.partner_id.id
#         return res
# 
#     def get_from_paypal_transaction_state(self, line_id):
#         st_obj = self.env['account.bank.statement.line']
#         st_line = st_obj.browse(line_id)
#         res = {}
#         print st_line.transaction_state
#         if st_line.transaction_state in BANK_FEE:
#             print "reco state", st_line.transaction_state
#             res['account_id'] = st_line.statement_id.profile_id.commission_account_id.id
#             res['partner_id'] = st_line.statement_id.profile_id.partner_id.id
#         return res
# 
#     def get_from_paypal_partner_email(self, cr, uid, line_id, context=None):
#         st_obj = self.pool['account.bank.statement.line']
#         st_line = st_obj.browse(cr, uid, line_id, context=context)
#         res = {}
#         partner_ids = st_obj.read_group(cr, uid,
#                                         [('email_from', '=', st_line.email_from),
#                                          ('partner_id', '!=', False)
#                                          ],
#                                         ['partner_id'],
#                                         ['partner_id'],
#                                         context=context)
#         if len(partner_ids) > 1:
#             return res
#         if partner_ids:
#             res['account_id'] = st_line.statement_id.profile_id.receivable_account_id.id
#             res['partner_id'] = partner_ids[0]['partner_id'][0]
#         return res
