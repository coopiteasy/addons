# -*- coding: utf-8 -*-
{
    'name': "Account Journal Lock Date",

    'summary': """
        Lock each journal independently""",

    'description': """
        Lock each journal independently.
        This is a backport of version 10.0 module of the same name by Stéphane Bidoul.
        
        https://github.com/OCA/account-financial-tools/tree/10.0/account_journal_lock_date
    """,

    'author': "Coop IT Easy SCRL",
    'website': "http://www.coopiteasy.be",

    'category': 'Accounting & Finance',
    'version': '9.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account'
    ],

    # always loaded
    'data': [
        'views/journal_lock_views.xml',
    ],
}
