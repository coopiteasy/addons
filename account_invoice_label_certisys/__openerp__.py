# -*- coding: utf-8 -*-
# Copyright 2013-2019 Coop IT Easy SCRLfs
#     - Houssine Bakkali <houssine@coopiteasy.be>
#     - Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice label certisys',
    'description': 'Add Certisys label on invoices, delivery slips and picking opperations (stock picking), and sale orders. This module should get a more generic name in the future.',
    'category': 'Invoice',
    'version': '9.0.1.1',
    'author': 'Coop IT Easy SCRLfs',
    "website": "https://coopiteasy.be",
    'depends': [
        'account',
        'stock',
        'sale',
        ],
    'data': [
        'reports/invoice_template.xml',
        'reports/stock_template.xml',
        'reports/sale_template.xml'
    ],
    'installable': True,
}
