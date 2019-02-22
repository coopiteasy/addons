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
    'website': "http://www.yourcompany.com",

    'category': 'Account',
    'depends': [
        'sale_stock',
    ],

    'data': [
        'views/stock_view.xml',
        'reports/report_deliveryslip.xml',
    ],
}
