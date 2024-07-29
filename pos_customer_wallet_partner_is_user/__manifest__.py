# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Point of Sale Customer Wallet Partner Is User",
    "summary": """
        Add a field on partners that shows whether they have used customer wallet
        functionality, and don't show some parts of customer wallet functionality
        to partners who haven't already used it.""",
    "version": "16.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "pos_customer_wallet",
    ],
    "excludes": [],
    "assets": {
        "point_of_sale.assets": [
            "pos_customer_wallet_partner_is_user/static/src/js/**/*.js",
            "pos_customer_wallet_partner_is_user/static/src/xml/**/*.xml",
        ],
    },
    "data": [
        "views/res_partner_views.xml",
    ],
    "demo": [],
}
