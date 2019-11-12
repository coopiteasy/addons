# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Sale Close',
    'description': """
        Allow to close the website for a moment and reopen it when needed.""",
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Coop IT Easy SCRLfs',
    'website': 'https://coopiteasy.be',
    'depends': [
        "website_sale",
        "website_payment",
    ],
    'data': [
        'views/website.xml',
        'templates/website_sale_close.xml',
    ],
    'demo': [
    ],
}
