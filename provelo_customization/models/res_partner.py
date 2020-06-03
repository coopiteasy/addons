# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    out_inv_comm_type = fields.Selection(default="bba")
    out_inv_comm_algorithm = fields.Selection(default="random")
