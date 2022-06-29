##############################################################################
#
#    OAC, Business Open Source Solution
#    Copyright (C) 2013-2016 Open Architects Consulting SPRL.
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
    "name": "Simple Payment reminder",
    "version": "12.0.1.0.0",
    "depends": ["account"],
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "category": "Accounting",
    "website": "https://coopiteasy.be",
    "summary": """
    This module just adds two fields to say when we sent a payment reminder to the
    customer and the level of the reminder.
    """,
    "data": [
        "views/invoice_view.xml",
    ],
}
