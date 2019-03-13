# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    active = fields.Boolean('Active', default=True)
