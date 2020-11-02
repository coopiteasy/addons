# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    _order = "date, time_start, id desc"

