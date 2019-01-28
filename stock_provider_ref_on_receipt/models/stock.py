# -*- coding: utf-8 -*-
from openerp import api, fields, models

class Stock(models.Model):
    _inherit = 'stock.picking'

    has_contract_hours = fields.Boolean(string="Has contract hours",
                                        compute="_compute_has_contract_hours")