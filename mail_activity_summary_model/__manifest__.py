# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Mail Activity Summary as a Model",
    "summary": """
        Instead of using a simple text field for the summary, use a model.""",
    "version": "12.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": ["mail"],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "views/mail_activity_views.xml",
    ],
    "demo": [],
    "qweb": [],
    "post_init_hook": "post_init_hook",
}
