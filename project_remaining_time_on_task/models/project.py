# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Task(models.Model):
    _inherit = 'project.task'
    remaining_hours_contract = fields.Float('Heures restantesc/ contrat', digits=(16,2), help="Total remaining time from the contract")
