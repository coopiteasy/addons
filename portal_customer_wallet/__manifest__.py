# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Portal Customer Wallet",
    "summary": """
        My Home displays expenditures using customer wallet""",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "portal",
        "website",
        "account_customer_wallet",
    ],
    "excludes": [],
    "data": [
        "views/portal_templates.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "portal_customer_wallet/static/src/css/portal_customer_wallet.css"
        ],
    },
}
