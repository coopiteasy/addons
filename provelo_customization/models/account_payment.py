# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountPayment(models.Model):
    _inherit = "account.payment"

    location_id = fields.Many2one(
        related="partner_id.resource_location",
        string="Location"
    )
