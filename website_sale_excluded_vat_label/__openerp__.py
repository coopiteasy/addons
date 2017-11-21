# -*- coding: utf-8 -*-
# © 2017- Houssine BAKKALI - Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Website Sale Excuded VAT Label',
    'version': '9.1.0.1',
    'category': 'E-commerce',
    'sequence': 95,
    'author': "Houssine BAKKALI - Coop IT Easy SCRLfs",
    'summary': 'Display the excluded vat label',
    'description': """

============================

This module add a commercial legal requirement concerning the price when it doesn't 
include the taxes. It is mandatory to add a label explaining that the price is 
taxes excluded 

    """,
    'depends': ['website_sale'],
    'data': [
        'views/website_sale_templates.xml',
    ],
    'installable': True,
}
