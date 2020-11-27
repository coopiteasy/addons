# -*- coding: utf-8 -*-
##############################################################################
#
#    Author Ludovic Lelarge
#    Copyright 2017 www.eta123.be
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
    'name': 'Accounting Winbooks Export',
    'version': '9.0.1.1.0',
    'depends': [
        'account',
    ],
    'author': "Ludovic Lelarge",
    'category': 'Accounting',
    'description': """

    Add a wizard that allow you to export data to Winbooks- Ajouter un wizard
    vous permettant d'exporter des données vers Winbooks

    - Factures Entries ACT.txt
    - Partenaires Entries CSF.txt
    - Analytics Entries ANT.txt

    You can filter by period

    """,
    'website': 'http://www.eta123.be',
    'license': 'AGPL-3',
    'data': [
        'wizard/account_winbooks_export_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
}
