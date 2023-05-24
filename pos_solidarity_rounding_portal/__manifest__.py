# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Point of Sale Solidarity Rounding Portal",
    "summary": """
        Allow registered users to change their solidarity rounding configuration in the
        account settings.""",
    "version": "12.0.1.0.0",
    "category": "Portal",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "pos_solidarity_rounding",
        "portal",
    ],
    "excludes": [],
    "data": [
        "views/portal_templates.xml",
    ],
    "demo": [],
    "qweb": [],
}
