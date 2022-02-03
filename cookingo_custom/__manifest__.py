# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "cookingo_custom",
    "summary": """
        Custom modifications for cookingo""",
    "version": "14.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "product",
        "uom_extra_data",  # mL
        "website_sale",
    ],
    "excludes": [],
    "data": [
        "data/portion_attributes.xml",
        "views/product_views.xml",
    ],
    "demo": [],
    "qweb": [],
}
