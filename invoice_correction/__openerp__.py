# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Account - Invoice Correction",
    "summary": "Correction of taxes and account on invoice",
    'description': "This module allow the account manager to correct invoice already validated",
    "version": "9.0.1.0.0",
    "license": "AGPL-3",
    "author": "Coopiteasy",
    "website": "http://www.coopiteasy.be",
    'category': 'Accounting',
    "depends": [
        "account",
    ],
    "data": [
        'views/invoice.xml'
    ],
    "installable": True,
}
