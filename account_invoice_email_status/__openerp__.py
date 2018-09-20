# -*- coding: utf-8 -*-
##############################################################################
#
#    Business Open Source Solution
#    Copyright (C) 2018 Coop IT Easy SCRLfs.
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
    "name": "Invoice Email Status",
    "version": "1.0",
    "depends": ["account"],
    "author": "Rémy Taymans <remy@coopiteasy.be>",
    "category": "CRM",
    "description": """
    This module add a column in the invoice list view to rapidly check
    if the invoice was send to the client or not.
    """,
    "license": "AGPL-3",
    'data': [
        'views/invoice_view.xml',
        'init_function.xml'
    ],
    'installable': True,
}
