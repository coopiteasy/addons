# -*- coding: utf-8 -*-
# Copyright (C) Kanak Infosystems LLP.

{
    'name': 'POS Mirror',
    'version': '1.0',
    'summary': 'POS Mirror',
    'description': """
POS Mirror
================================
    """,
    'author': 'Kanak Infosystems LLP.',
    'category': 'Point of Sale',
    'images': ['static/description/main_screenshot.png'],
    'depends': ['point_of_sale', 'website'],
    'data': [
        'views/pos_assets.xml',
        'views/pos_mirror_view.xml',
        'views/pos_mirror_template.xml',
        'data/data.xml'
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': False,
    'price' : 99,
    'currency': 'EUR',
}
