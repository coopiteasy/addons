# -*- coding: utf-8 -*-

from openerp import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    warehousekeeper_nb = fields.Char(
        string="Authorized Warehousekeeper Number"
    )
