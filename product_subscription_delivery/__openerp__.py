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
    "name": "Product Subscription Delivery",
    "version": "1.0",
    "depends": [
        "product_subscription",
        "delivery",
    ],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Sales",
    "description": """
    This module allows to manager delivery method on production subscription to have
    it set on the invoice without passing by the sale order..
    """,
    'data': [
        'views/subscription_views.xml',
    ],
    'installable': True,
}