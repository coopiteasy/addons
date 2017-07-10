# -*- coding: utf-8 -*-
# Copyright 2017 Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Global discount on invoice',
    'version': '9.0.1.1.0',
    'author': 'Houssine BAKKALI - Coop IT Easy',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'website': 'https://www.coopiteasy.be',
    'depends': [
        'account',
    ],
    "description": """
    this module give global discount on invoice. It allows to set a the same discount on all the invoice line without been forced to go manually through all the lines.    
    """,
    'data': [
        'views/account_invoice_view.xml'
    ],
    'installable': True,
}
