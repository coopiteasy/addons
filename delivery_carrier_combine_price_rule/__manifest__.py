# Copyright 2022 Coop IT Easy SC, Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Delivery Carrier Combine Price Rule",
    "summary": """
        Chose how to combine price rule on a delivery carrier.""",
    "version": "12.0.1.0.0",
    "category": "Stock",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": ["delivery"],
    "excludes": [],
    "data": ["views/delivery_carrier.xml"],
    "demo": ["demo/delivery_carrier.xml"],
    "qweb": [],
}
