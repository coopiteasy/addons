# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Point of Sale Solidarity Rounding Portal",
    "summary": """
        Allow registered users to change their solidarity rounding configuration in the
        account settings.""",
    "version": "16.0.1.0.0",
    "category": "Portal",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "depends": [
        "pos_solidarity_rounding",
        "portal",
    ],
    "data": [
        "views/portal_templates.xml",
    ],
}
