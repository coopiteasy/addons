# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Supplier Free Shipping Threshold",
    "summary": """
        Free Shipping Threshold On Suppliers""",
    "version": "12.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": ["purchase"],
    "excludes": [],
    "data": [
        "views/purchase_order.xml",
        "views/res_partner.xml",
    ],
    "demo": [],
    "qweb": [],
}
