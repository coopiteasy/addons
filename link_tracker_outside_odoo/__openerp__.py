# -*- coding: utf-8 -*-
# © 2017- Houssine BAKKALI - Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Link tracker outside Odoo',
    'version': '9.0.0.1',
    'category': 'Marketing',
    'sequence': 95,
    'author': "Houssine BAKKALI - Coop IT Easy SCRLfs",
    'website': 'www.coopiteasy.be',
    'license': "AGPL-3",
    'summary': 'Return a proper redirect url when the domain is not manager by Odoo',
    'description': """

============================

This module fix the redirect url when the domain is not managed by Odoo with that it lead to broken links 

    """,
    'depends': ['link_tracker'],
    'data': [],
    'installable': True,
}
