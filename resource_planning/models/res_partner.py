# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_default_location(self):
        location = self.env.user.resource_location
        if not location:
            main_location = self.env.ref(
                "resource_planning.main_location", False
            )
            return (
                main_location
                if main_location
                else self.env["resource.location"]
            )
        return location

    resource_location = fields.Many2one(
        "resource.location",
        string="Location",
        default=_get_default_location,
        domain=[("main_location", "=", True)],
    )
