# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class HrExpense(models.Model):

    _inherit = "hr.expense"

    expense_type = fields.Selection([
                    ("car_travel", "Car/Motorbike travel"), 
                    ("transport_ticket", "Transport ticket"),
                    ("miscellaneous","Miscellaneous")], default='car_travel', 
                    states={'done': [('readonly', True)], 'post': [('readonly', True)]}, 
                    string="Expense type")
