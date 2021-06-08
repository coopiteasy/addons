# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Resource Stock Information",
    "version": "9.0.1.0.1",
    "depends": [
        "resource_planning",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Resource",
    "website": "https://www.coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
        Track resources movement in and out of stock.
    """,
    "data": [
        "views/resource_views.xml",
    ],
    "installable": True,
    "application": True,
}
