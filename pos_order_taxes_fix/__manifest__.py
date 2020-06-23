# Copyright 2019 Coop IT Easy SCRL fs
#   Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "POS orders taxes fix",
    "summary": """
        Adds a button to on pos session to fix the taxes of the orders that
        doesn't match the calculation on backend"
    """,
    "author": "Coop IT Easy SCRL fs",
    "website": "www.coopiteasy.be",
    "category": "Point of Sale",
    "version": "12.0.1.0.0",
    "depends": ["point_of_sale"],
    "data": ["views/pos_session_view.xml"],
    "demo": [],
    "installable": True,
    "license": "AGPL-3",
}
