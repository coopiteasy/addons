# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class ResourceLocation(models.Model):
    _name = 'resource.location'
    
    name = fields.Char(string="Name")
    address = fields.Many2one('res.partner', string="Address")

