# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Website Sale Product Trial",
    "summary": """
        Configure product contract to be a trial subscription.""",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "website_sale_product_compatibility",
        "product",
        "delivery",
    ],
    "excludes": [],
    "data": [
        "views/product_views.xml",
        "views/templates.xml",
    ],
    "demo": [],
    "qweb": [],
}
