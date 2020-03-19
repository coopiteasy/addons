# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    terms_conditions_ids = fields.One2many(
        comodel_name="res.company.terms",
        inverse_name="company_id",
        string="Terms and Conditions",
    )
