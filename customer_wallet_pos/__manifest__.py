# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Point of Sale Customer Wallet",
    "summary": """
        Enable usage of the Customer Wallet in the Point of Sale.""",
    "version": "16.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC,GRAP",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "point_of_sale",
        "customer_wallet_account",
    ],
    "excludes": [],
    "assets": {
        "point_of_sale.assets": [
            "customer_wallet_pos/static/src/css/pos.css",
            "customer_wallet_pos/static/src/js/**/*.js",
            "customer_wallet_pos/static/src/xml/**/*.xml",
        ],
    },
    "data": [],
    "demo": [
        "demo/pos_payment_method_demo.xml",
        "demo/product_product_demo.xml",
    ],
}
