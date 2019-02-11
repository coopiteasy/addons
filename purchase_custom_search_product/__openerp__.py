# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
# Nicolas Jamoulle, <nicolas@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Custom search product for purchase lines",
    "version": "1.0",
    "depends": [
        'purchase',
    ],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "website": "www.coopiteasy.be",
    "description": """
        Do not allow to add product mark as 'Cannot be buy'
    """,
    "data": [
        'views/purchase_view.xml',
    ],
    'installable': True,
}
