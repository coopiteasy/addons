# Copyright 2021 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Picking Mail Incorrect Quantity",
    "description": """
        Send an e-mail about incorrect amounts received when confirming a stock picking.""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://coopiteasy.be",
    "category": "Sales Management",
    "depends": [
        "mail",
        "stock",
    ],
    "data": [
        "data/mail_template.xml",
    ],
    "demo": [],
}
