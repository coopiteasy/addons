# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2011 Noviat nv/sa (www.noviat.be). All rights reserved.
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
    'name': 'Belgium - Import Bank CODA Statements',
    'version': '2.1',
    'author': 'University of Namur',
    'category': 'Accounting & Finance',
    'description': '''
Module to import CODA bank statements.
======================================

Supported are CODA flat files in V2 format from Belgian bank accounts.
----------------------------------------------------------------------
    * CODA v1 support.
    * CODA v2.2 support.
    * Foreign Currency support.
    * Support for all data record types (0, 1, 2, 3, 4, 8, 9).
    * Parsing & logging of all Transaction Codes and Structured Format
      Communications.
    * Support for multiple Journals per Bank Account Number.
    * Support for multiple statements from different bank accounts in a single
      CODA file.

The machine readable CODA Files are parsed and Bank Statements are generated containing a subset of
the CODA information (only those transaction lines that are required for the
creation of the Financial Accounting records).

Remark on CODA V1 support:
~~~~~~~~~~~~~~~~~~~~~~~~~~
In some cases a transaction code, transaction category or structured
communication code has been given a new or clearer description in CODA V2.The
description provided by the CODA configuration tables is based upon the CODA
V2.2 specifications.
If required, you can manually adjust the descriptions via the CODA configuration menu.
''',
    'depends': ['account_accountant', 'account_bank_statement_import', 'l10n_be'],
    'demo': [
    ],
    'data': [
        'views/l10n_be_coda_view.xml',
        'views/bank_statement_line_view.xml'
    ],
    'auto_install': False,
    'website': 'https://www.odoo.com/page/accounting',
    'installable': True,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
