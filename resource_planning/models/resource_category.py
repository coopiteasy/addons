# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResourceCategory(models.Model):
    _name = "resource.category"
    _inherit = "mail.thread"

    name = fields.Char(string="Category name", required=True, translate=True,)
    resources = fields.One2many(
        "resource.resource", "category_id", string="Resources"
    )
    is_accessory = fields.Boolean(string="Is Accessory")

    active = fields.Boolean(
        "Active", default=True, track_visibility="onchange"
    )
