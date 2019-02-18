# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
# Nicolas Jamoulle, <nicolas@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Global discount on invoice',
    'version': '1.0',
    'author': 'Coop IT Easy SCRLfs',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'website': 'https://www.coopiteasy.be',
    'depends': [
        'account',
    ],
    "description": """
        New field added to give the structured communication of the invoice partner
    """,
    'data': [
        'views/account_invoice_view.xml'
    ],
    'installable': True,
}
