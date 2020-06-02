# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class SaleNote(models.Model):
    _name = "res.company.note"
    _description = "Sale Note"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env["res.company"]._company_default_get(),
    )
    name = fields.Char(string="Name", required="True")
    content = fields.Html(
        string="Content", required="True", translate=True, sanitize=False
    )
    active = fields.Boolean(string="Active", default=True)
