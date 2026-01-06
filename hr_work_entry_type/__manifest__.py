# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Work Entry Type",
    "summary": "Add list view for  hr.work.entry.type",
    "version": "18.0.1.0.0",
    "category": "Human Resources/Employees",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["mihien"],
    "license": "AGPL-3",
    "depends": [
        "hr",
        "hr_work_entry",
        "hr_work_entry_holidays",
    ],
    "data": [
        "views/hr_work_entry_type_views.xml",
        "views/hr_views.xml",
    ],
}
