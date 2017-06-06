# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 - Coop IT Easy.
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
    "name": "Respond to mail on price list",
    "version": "1.0",
    "depends": ["product",],
    "author": "Houssine BAKKALI <houssine.bakkali@gmail.com>",
    "category": "Invoice",
    "description": """
    This module allow to set an email address on the price list 
    in order to have specific respond to address mail for the mail sent. 
    """,
    'data': [
        'views/pricelist_view.xml',
    ],
    'installable': True,
}