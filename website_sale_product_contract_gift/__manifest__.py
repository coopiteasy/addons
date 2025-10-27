# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Website Sale Product Contract Gift",
    "summary": """
        Configure product contract to be a gift to someone else.""",
    "version": "16.0.1.1.0",
    "category": "Website",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "website_sale_product_compatibility",
        "product_contract",
        "delivery",
        "account_payment_sale",
    ],
    "data": [
        "views/product_views.xml",
        "views/templates.xml",
        "views/sale_order_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_product_contract_gift/static/src/js/website_sale.esm.js",
        ],
    },
}
