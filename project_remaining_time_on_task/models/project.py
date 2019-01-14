# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Task(models.Model):
    _inherit = 'project.task'

    # fields.function(_compute_remaining_hours_contract,'Heures restantes / contrat', digits=(16, 2),
    #                                     help="Total remaining time from the contract")

    def _compute_remaining_hours_contract(self):
        return 2.0

    remaining_hours_contract = fields.function(_compute_remaining_hours_contract, 'Heures restantes / contrat',
                                               type='digits=(16, 2)')
