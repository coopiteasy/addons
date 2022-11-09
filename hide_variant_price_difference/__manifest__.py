# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "hide_variant_price_difference",
    "summary": """
        On website sale views, hide the tags next to product variants that show
        the price difference compared to the current price.""",
    "version": "14.0.1.0.1",
    "category": "Website",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "sale",
        "website_sale",
    ],
    "excludes": [],
    "data": ["views/templates.xml"],
    "demo": [],
    "qweb": [],
}
