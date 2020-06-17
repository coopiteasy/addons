# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProVeloFinancing(models.Model):
    _name = "pv.financing"

    name = fields.Char()
    bob_code = fields.Char(string="Bob Code")
