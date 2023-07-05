# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Point of Sale Customer Wallet",
    "summary": """
        Enable usage of the Customer Wallet in the Point of Sale.""",
    "version": "13.0.1.0.0",
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
    "data": [
        "templates/assets.xml",
    ],
    "demo": [
        "demo/product_product_demo.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
}
