# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    date_start = fields.Datetime()
    plan_date_start = fields.Datetime()
    is_milestone = fields.Boolean()
    resource_id = fields.Many2one("res.users", compute="_compute_resource_id")
    completion = fields.Float()
    is_parent = fields.Boolean(compute="_compute_is_parent")
    is_expanded = fields.Boolean(compute="_compute_is_parent")
    caption = fields.Char()
    notes = fields.Char()
    cost = fields.Float()
    bar_text = fields.Char()

    @api.depends("user_ids")
    def _compute_resource_id(self):
        for record in self:
            if record.user_ids:
                record.resource_id = record.user_ids[0]
            else:
                record.resource_id = False

    @api.depends("child_ids")
    def _compute_is_parent(self):
        for record in self:
            record.is_parent = bool(record.child_ids)
            record.is_expanded = record.is_parent
