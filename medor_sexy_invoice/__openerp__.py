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
    "name": "Medor Sexy Invoice",
    "version": "1.0",
    "depends": ["base",
                "account",
                "theme_light"],
    "author": "Houssine BAKKALI <houssine.bakkali@gmail.com>",
    "category": "Invoice",
    "description": """
    This module adapts the invoice to the Medor look & feel.
    """,
    'data': [
        'report/docs_report.xml',
        'report/sexy_invoice.xml',
    ],
    'installable': True,
}