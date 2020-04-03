# Copyright 2020-      Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner BVR',
    'version': '11.0.1.0.0',
    'depends': [
        'base',
        'sale'
    ],
    'author': 'Coop IT Easy SCRLfs',
    'category': 'Sales',
    'website': 'https://www.coopiteasy.be',
    'license': 'AGPL-3',
    'description': """
    This module adds BVR number on res partner
    """,
    'data': [
        'data/customer_id_sequence.xml',
        'views/partner_view.xml',
    ],
    'installable': True,
}
