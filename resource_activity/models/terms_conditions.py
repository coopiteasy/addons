# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class TermsConditions(models.Model):
    _name = "res.company.terms"
    _description = "Terms and Conditions"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )

    name = fields.Char(string="Name", required="True")
    content = fields.Html(string="Content", required="True")
    active = fields.Boolean(string="Active", default=True)
