# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResourceActivityRegistration(models.Model):
    _inherit = ["resource.activity.registration"]

    is_paid = fields.Boolean(
        string="Paid",
    )

    @api.multi
    def mark_as_paid(self):
        for registration in self:
            registration.is_paid = True
