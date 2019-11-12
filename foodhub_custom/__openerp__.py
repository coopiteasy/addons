# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
# 	    Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Foodhub Custom",
    'version': '9.0.1.0.0',
    'description': """
        Foodhub customizations""",

    'author': "Coop IT Easy SCRL fs",
    'website': "http://www.coopiteasy.be",
    'license': 'AGPL-3',
    'category': 'Account',
    'depends': [
        'sale_stock',
        'sale_order_volume',
    ],

    'data': [
        'reports/report_deliveryslip.xml',
        'views/templates.xml',
    ],
}
