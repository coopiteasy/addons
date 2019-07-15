# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Stock Picking Copy Quantity",

    'summary': """
        Adds a button to copy reserved quantity to received quantity    
    """,

    'author': "Beescoop - Cellule IT, Coop IT Easy SCRL fs",
    'website': "https://github.com/beescoop/Obeesdoo",

    'category': 'Sales Management',
    'version': '9.0.0.0.1',

    'depends': [
        'stock',
    ],

    # always loaded
    'data': [
        'views/stock.xml',
    ],

    'demo': [],
}
