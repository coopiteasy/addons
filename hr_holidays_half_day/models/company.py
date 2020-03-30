# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    hours_per_day = fields.Float(
        string="Company Hours Per Day",
        required=True,
        digits=(2, 2),
        default=7.6,
    )

    am_hour_from = fields.Float(
        string="AM Work from", required=True, digits=(2, 2), default=8.7
    )

    am_hour_to = fields.Float(
        string="AM Work to", required=True, digits=(2, 2), default=12.5
    )

    pm_hour_from = fields.Float(
        string="PM Work from", required=True, digits=(2, 2), default=13.5
    )

    pm_hour_to = fields.Float(
        string="PM Work to", required=True, digits=(2, 2), default=17.3
    )
