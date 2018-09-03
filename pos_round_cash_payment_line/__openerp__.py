# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017- Coop IT Easy.
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
    "name": "Pos Round Cash Payment Line",
    "version": "9.0.0.1.0",
    "author": "Coop IT Easy - Robin Keunen <robin@coopiteasy.be>",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "website": "www.coopiteasy.be",
    "description": """
        Rounds due amount to nearest 5 cents when adding a cash Payment line.
        An line is added on the invoice to record the rounding remainder.
        
        The product *Round Remainder Product* is added to your product list.
        You must set the Rounding Account through:
        - Round Remainder Product > Accounting 
          - > Income Account
          - > Expense Account
        
    """,
    "depends": [
        'point_of_sale',
        'product',
    ],
    'data': [
        'views/pos_config.xml',
        'data/round_remainder_product.xml',
        'static/src/xml/templates.xml',
    ],
    'qweb': [
        'static/src/xml/pos_round_cash_payment_line.xml'
    ],
    'installable': True,
}
