# -*- coding: utf-8 -*-

# Copyright 2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Communication Tag',

    'summary': """
    Let you add tags to a contact to manage your communication
    strategies.
    """,
    'description': """
    """,

    'author': 'Rémy Taymans',
    'license': 'AGPL-3',
    'version': '9.0.1.0',
    'website': "https://github.com/houssine78/addons",

    'category': '',

    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/partner_communication_tag.xml',
    ]
}
