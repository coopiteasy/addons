# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Thibault François
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    pr_uri = fields.Char(string="PR URI")
    int_priority = fields.Integer(string="Priority", default=99)
    author_id = fields.Many2one("res.users", string="Author")
    reviewer_id = fields.Many2one("res.users", string="Reviewer")
    tester_id = fields.Many2one("res.users", string="Tester")
    link_task_ids = fields.Many2many(
        comodel_name="project.task",
        relation="link_task_relation_table",
        column1="user1_id",
        column2="user2_id",
        string="Linked Tasks",
    )
