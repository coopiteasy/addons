# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResourceActivityLang(models.Model):
    _name = "resource.activity.lang"

    name = fields.Char(
        string="Lang",
        required=True,
        translate=True,
    )
    code = fields.Char(string="Code")
    active = fields.Boolean("Active", default=True)
