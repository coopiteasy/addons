# Copyright 2017 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Check Identical Invoice",
    "version": "12.0.1.0.0",
    "depends": [
        'base',
        'account',
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Accounting & Finance",
    "website": "https://coopiteasy.be",
    "description": """
        This module requires to check this box to validate the invoice 
        if invoices with the same partner, invoice date and totam alount already
        exist.
    """,
    'data': [
        "views/account_invoice.xml",
    ],
    'installable': True,
}
