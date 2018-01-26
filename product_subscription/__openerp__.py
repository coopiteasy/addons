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
    "name": "Product Subscription",
    "version": "1.0",
    "depends": [
        "sale",
        "partner_firstname",
        "account_analytic_distribution",
        "l10n_be_invoice_bba",
        "email_template_config",
    ],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Sales",
    "description": """
    This module manages the subscription for a quantity of product 
    for which we need to invoice the whole amount at the subscription time
    and the delivery needs to be splited in the time. This module has been 
    developed for a magazine that publish a new edition every 3 months.
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/product_subscription_data.xml',
        'views/subscription_views.xml',
        'views/product_views.xml',
        'views/res_partner_views.xml',
        'views/product_release_view.xml',
    ],
    'installable': True,
}