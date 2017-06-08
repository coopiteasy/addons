# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class AccountJournal(models.Model):
    
    _inherit = 'account.journal'

    email = fields.Char(string="Respond to")