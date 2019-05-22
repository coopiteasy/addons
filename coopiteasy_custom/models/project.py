# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    pr_uri = fields.Char(
        string='PR URI')
    int_priority = fields.Integer(
        string='Priority',
        default=99,
    )
