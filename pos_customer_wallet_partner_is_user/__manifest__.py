# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Point of Sale Customer Wallet Partner Is User",
    "summary": """
        Add a field on partners that shows whether they have used customer wallet
        functionality, and don't show some parts of customer wallet functionality
        to partners who haven't already used it.""",
    "version": "12.0.1.1.0",
    "category": "Point of Sale",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainer": "Coop IT Easy SC",
    "maintainers": ["coopiteasy"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "pos_customer_wallet",
    ],
    "excludes": [],
    "data": [
        "templates/assets.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
}
