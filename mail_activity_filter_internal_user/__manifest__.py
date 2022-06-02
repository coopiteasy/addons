# SPDX-FileCopyrightText: 2022 Coop IT Easy SCRLfs
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Mail Activity Filter Internal User",
    "summary": """
        Filter on internal user by default when assigning someone to an activity.""",
    "version": "12.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "depends": ["mail"],
    "excludes": [],
    "data": [
        "views/mail_activity.xml",
    ],
    "demo": [],
    "qweb": [],
}
