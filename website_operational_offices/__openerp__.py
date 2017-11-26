# -*- coding: utf-8 -*-
# © 2017- Houssine BAKKALI - Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Website Operational Sites',
    'version': '9.1.0.1',
    'category': 'Website',
    'sequence': 95,
    'author': "Houssine BAKKALI - Coop IT Easy SCRLfs",
    'summary': 'Display the operational sites on the contact page',
    'description': """

============================

This module allows to define operational sites and to display them
on the contact page 

    """,
    'depends': [
        'base',
        'website'
    ],
    'data': [
        'views/website_templates.xml',
        'views/res_company_view.xml',
    ],
    'installable': True,
}
