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
    "name": "Account Invoice Check Identical Invoice",
    "version": "1.0",
    "depends": [
        "base",
        "account",
    ],
    "author": "Robin Keunen <robin@coopiteasy.be>",
    "category": "",
    "website": "www.coopiteasy.be",
    "description": """
        This module requires to check this box to validate the invoice 
        if invoices with the same partner, invoice date and totam alount already
        exist.
    """,
    "data": [
        "views/account_invoice.xml",
    ],
    "installable": True,
}
