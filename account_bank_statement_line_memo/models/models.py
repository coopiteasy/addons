# -*- coding: utf-8 -*-

from openerp import models, fields


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    name = fields.Char(
        string='Memo',
        required=False,
        default="",
    )
