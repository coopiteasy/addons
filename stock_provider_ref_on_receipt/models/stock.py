# -*- coding: utf-8 -*-
from openerp import api, fields, models


class Stock(models.Model):
    _inherit = 'stock.picking'

    provider_ref_id = fields.Char(string="Provider Reference")
