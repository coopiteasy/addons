# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Restrict SEPA Direct Debit Payment",
    "summary": """
        Restrict payment by SEPA Direct Debit for some products.""",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "website_sale_sepa_dd_payment",
    ],
    "excludes": [],
    "data": [
        "views/product_views.xml",
        "views/templates.xml",
    ],
    "demo": [],
    "qweb": [],
}
