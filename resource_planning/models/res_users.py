# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    resource_location = fields.Many2one("resource.location", string="Location")
