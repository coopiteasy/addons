# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019 Coop IT Easy
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
    "name": "POS Search Accented/Unaccented Characters",
    "version": "9.0.1.0.0",
    "depends": [
        "point_of_sale",
    ],
    "author": "Vincent Van Rossem <vincent@coopiteasy.be>",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "website": "www.coopiteasy.be",
    "description": """
        Allows to search in POS for products using accented and/or unaccented characters.
    """,
    "data": [
        'views/templates.xml',
    ],
    'installable': True,
}
