# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResourceLocation(models.Model):
    _inherit = "resource.location"

    guides = fields.One2many(
        "res.partner",
        "resource_location_guide",
        domain=[("is_guide", "=", True)],
        string="Guides",
    )
    trainers = fields.One2many(
        "res.partner",
        "resource_location_trainer",
        domain=[("is_trainer", "=", True)],
        string="Trainers",
    )
    opening_hours_ids = fields.Many2many(
        "activity.opening.hours", string="Opening Hours"
    )
    terms_ids = fields.One2many("resource.location.terms", "location_id")
