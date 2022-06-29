# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Delivery Product Restriction",
    "summary": """
        Allow some product to be shipped only by some delivery carrier.""",
    "version": "12.0.1.0.0",
    "category": "Delivery",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": ["sale", "delivery"],
    "excludes": [],
    "data": [
        "views/product_template.xml",
    ],
    "demo": [],
    "qweb": [],
}
