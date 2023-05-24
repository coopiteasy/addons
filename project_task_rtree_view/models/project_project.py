# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    parent_id = fields.Many2one("project.project", string="Parent Project", index=True)
