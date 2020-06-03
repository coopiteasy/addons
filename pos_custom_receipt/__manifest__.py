# Copyright 2019-Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "POS Custom Receipt",
    "version": "12.0.1.0.0",
    "depends": [
        "point_of_sale",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Point Of Sale",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This module extends the pos receipt in order to hide some info and
    adds other info.
    """,
    'data': [],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
}
