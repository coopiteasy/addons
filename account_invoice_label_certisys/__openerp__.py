# -*- coding: utf-8 -*-
##############################################################################
#
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
    'name': 'Account Invoice label certisys',
    'description': 'Add Certisys label on invoices, delivery slips and picking opperations (stock picking), and sale orders',
    'category': 'Invoice',
    'version': '9.0.1.0',
    'author': 'Coop IT Easy SCRLfs',
    'depends': [
        'account',
        ],
    'data': [
        'reports/invoice_template.xml',
        'reports/stock_template.xml',
        'reports/sale_template.xml'
    ],
    'installable': True,
}
