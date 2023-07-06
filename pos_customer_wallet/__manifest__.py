# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Point of Sale Customer Wallet",
    "summary": """
        Enable usage of the Customer Wallet in the Point of Sale.""",
    "version": "15.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC,GRAP",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "point_of_sale",
        "account_customer_wallet",
    ],
    "excludes": [],
    "assets": {
        "point_of_sale.assets": [
            "pos_customer_wallet/static/src/css/pos.css",
            "pos_customer_wallet/static/src/js/models.js",
            "pos_customer_wallet/static/src/js/screens.js",
        ],
        "web.assets_qweb": [
            "pos_customer_wallet/static/src/xml/pos.xml",
        ],
    },
    "data": [],
    "demo": [
        "demo/product_product_demo.xml",
    ],
}
