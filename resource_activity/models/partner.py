# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_guide = fields.Boolean(string="Guide")
    is_trainer = fields.Boolean(string="Trainer")


