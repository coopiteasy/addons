# -*- coding: utf-8 -*-
from openerp import fields, models


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    reminder = fields.Selection([('1', 'Premier rappel'),
                                 ('2', 'Second rappel'),
                                 ('3', 'Troisieme rappel'),
                                 ('4', 'Recommande')], string="Rappel")
    last_reminder_date = fields.Date(string="Date du dernier rappel")
