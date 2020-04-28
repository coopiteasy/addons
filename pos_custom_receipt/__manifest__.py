# Copyright 2019-Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "POS Custom Receipt",
    "version": "11.0.1.0.0",
    "depends": [
        "point_of_sale",
    ],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "POS",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This module extends the pos receipt in order to not show some info and
    adds other info.
    """,
    'data': [],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
}
