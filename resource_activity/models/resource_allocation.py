# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResourceAllocation(models.Model):
    _inherit = "resource.allocation"

    activity_registration_id = fields.Many2one(
        "resource.activity.registration",
        string="Activity registration",
        readonly=True,
    )
    activity_id = fields.Many2one(
        related="activity_registration_id.resource_activity_id",
        string="Activity",
        readonly=True,
    )
