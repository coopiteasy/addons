# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "E-commerce Subscription Form",
    "summary": """
        Form to order subscription product""",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "website_sale",
        "product_contract",
    ],
    "excludes": [],
    "data": [
        "views/templates.xml",
    ],
    "demo": [],
    "qweb": [],
}
