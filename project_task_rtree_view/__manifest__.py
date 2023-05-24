# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Task RTree View",
    "summary": "Use the rtree view as a default view for tasks",
    "version": "16.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "project",
        "web_view_rtree",
    ],
    "data": [
        "views/project_project_view.xml",
        "views/project_task_view.xml",
    ],
}