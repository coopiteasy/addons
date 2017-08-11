# -*- coding: utf-8 -*-
# © 2017 Houssine BAKKALI, Coop IT Easy
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Product to scale bizerba extended",
    'summary': """
        This module gather the extension to the module product_to_scale_bizerba.
    """,
    'author': 'Houssine BAKKALI, Coop IT Easy',
    'category': 'Sales',
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'depends': ['product','product_to_scale_bizerba'],
    'data': [
        'views/product_view.xml', 
        'views/product_scale_log_view.xml',        
    ],
}
