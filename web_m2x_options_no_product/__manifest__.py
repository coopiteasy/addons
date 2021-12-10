# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "web_m2x_options_no_product",
    "description": """
        Removes creation options from (some) product dropdown menus.""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://coopiteasy.be",
    "depends": [
        "web_m2x_options",
        "account",
        "purchase",
        "sale",
        "stock",
    ],
    "data": [
        "views/account.xml",
        "views/purchase.xml",
        "views/sale.xml",
        "views/stock.xml",
    ],
    "demo": [],
}
