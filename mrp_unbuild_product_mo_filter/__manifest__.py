# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Filter unbuild MO by product",
    "summary": "Filter unbuild manufacturing orders by selected product",
    "version": "12.0.1.0.1",
    "category": "Manufacturing",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "mrp",
    ],
    "excludes": [],
    "data": [
        "views/mrp_unbuild.xml",
    ],
    "demo": [],
    "qweb": [],
}
