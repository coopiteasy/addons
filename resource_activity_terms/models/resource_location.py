# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResourceLocation(models.Model):
    _inherit = "resource.location"

    terms_ids = fields.One2many("resource.location.terms", "location_id")
