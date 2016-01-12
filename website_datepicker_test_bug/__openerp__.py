# -*- coding: utf-8 -*-
##############################################################################
#
#    Open Architects Consulting, Business Open Source Solution
#    Copyright (C) 2013-2016 Open Architects Consulting sprl.
#    Author : Houssine BAKKALI
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
    'name': 'website sale datepicker test',
    'description': 'This module test a bug with datepicker function',
    'category': 'E-Commerce',
    'version': '1.0',
    'author': 'Houssine BAKKALI',
    'depends': ['website_sale','website_sale_delivery','sale_order_dates'],
    'data': [
        'views/templates.xml',
    ],
    'installable' : True,
}