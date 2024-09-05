# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Multi-week calendars with work time from contracts",
    "summary": """
        A compatibility module.""",
    "version": "12.0.1.0.0",
    "category": "Hidden",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "resource_multi_week_calendar",
        "resource_work_time_from_contracts",
    ],
    "auto_install": True,
    "data": [
        "views/hr_contract_views.xml",
    ],
}
