# -*- coding: utf-8 -*-
# © 2017- Houssine BAKKALI - Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Expense Type v10',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 95,
    'author': "Houssine BAKKALI - Coop IT Easy SCRLfs",
    'summary': 'Type Expenses',
    'description': """
Manage expenses the expense types
============================

This application allows you to add type to the expense. In this way you will be able to organize your expense by type on the different report

    """,
    'depends': ['hr_expense_v10'],
    'data': [
        'views/hr_expense_views.xml',
    ],
    'installable': True,
}
