# -*- coding: utf-8 -*-
# © 2016 Houssine BAKKALI, Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Purchase order status",
    'summary': """
        This module implements new fields and modify the invoice_status in
        order to give a better view on the purchase order status.
    """,
    'author': 'Coop IT Easy SCRLfs',
    'website': 'www.coopiteasy.be',
    'category': 'Purchase Management',
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'depends': ['purchase'],
    'data': [
        'views/purchase_view.xml',
    ],
}
