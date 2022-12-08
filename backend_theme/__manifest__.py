# Copyright 2016 Openworx, LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Community Mobile Backend Theme",
    "version": "11.0.1.0.2",
    "category": "Themes/Backend",
    "website": "https://coopiteasy.be",
    "summary": """
        Backend theme for Odoo 10.0 Community Edition (based on Openworx Theme).
        More polished and added some responsive CSS rules.
    """,
    "images": ["images/screen.png"],
    "author": "Farrell Rafi, Coop IT Easy SC",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "web",
    ],
    "data": [
        "views/assets.xml",
        "views/web.xml",
    ],
}
