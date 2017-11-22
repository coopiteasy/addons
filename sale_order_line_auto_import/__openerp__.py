# -*- coding: utf-8 -*-
# © 2016 Houssine BAKKALI, Coop IT Easy SCRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Sale order line auto import",
    'summary': """
        This module allows to create automatically line with the product 
        when selecting the partner. The user can then delete the line that he doesn't want and
        update the quantity on each line.
    """,
    'author': 'Houssine BAKKALI, Coop IT Easy SCRL',
    'category': 'Sales',
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'depends': ['sale',],
    'data': [
        'views/sale_order_view.xml',
    ],
}

