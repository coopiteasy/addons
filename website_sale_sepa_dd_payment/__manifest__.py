# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "E-commerce SEPA Direct Debit Payment for specific products",
    "summary": """
        Pay via SEPA Direct Debit for some products.""",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "website_sale",
        "payment_custom",
    ],
    "excludes": [],
    "data": [
        "views/product_views.xml",
        "views/templates.xml",
        "data/payment_provider_data.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_sepa_dd_payment/static/src/js/payment_form.js",
        ],
    },
    "demo": [],
    "qweb": [],
}
