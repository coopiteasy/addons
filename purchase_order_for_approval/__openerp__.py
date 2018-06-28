# -*- coding: utf-8 -*-
# © 2017- Robin Keunen - Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Order - For Approval Mention',
    'version': '9.1.0.1',
    'category': 'Sales',
    'sequence': 95,
    'author': "Robin KEUNEN- Coop IT Easy SCRLfs",
    'summary': 'Display "For Approval" mention on Purchase Orders',
    'description': """

============================

This module adds a "For approval section to purchase orders"

    """,
    'depends': ['sale'],
    'data': [
        'views/report_saleorder.xml',
    ],
    'installable': True,
}
