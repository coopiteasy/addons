# -*- coding: utf-8 -*-
##############################################################################
#
#    Business Open Source Solution
#    Copyright (C) 2013-2016 Coop IT Easy SCRL.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Delivery distribution Management",
    "version": "1.0",
    "depends": [
            "sale",
            "account",
            "sale_stock",
    ],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Sales",
    "description": """
    This module manage the distribution of a product on a through all the sale/deposit 
    points, it manages the recurring order through the list of distribution.    
    """,
    'data': [
        'security/delivery_distribution_list_security.xml',
        'security/ir.model.access.csv',
        'data/ddl_data.xml',
        'views/partner_view.xml',
        'views/sale_view.xml',
        'views/delivery_distribution_list_view.xml',
        'views/stock_view.xml',
        'views/product_view.xml',
        'report/sale_order_report_template.xml',
        'report/report_deliveryslip.xml',
    ],
    'installable': True,
}