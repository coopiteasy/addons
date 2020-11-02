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
    "name": "Provelo Customization",
    "version": "9.0.1.1.0",
    "depends": [
        "csv_export_invoice",
        "csv_export_partner",
        "csv_export_payment",
        "hr_holidays",
        "hr_timesheet_sheet",
        "resource_planning",
        "resource_activity",
        "web_readonly_bypass",
        "l10n_be_invoice_bba",
        "account_archive_journals",
    ],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "category": "",
    "website": "www.coopiteasy.be",
    "description": """
        * default value on invoice policy to order
        * default value on res_partner out_inv_comm_type to bba
        * default value on res_partner out_inv_comm_algorithm to random
        * automatic validation of invoices
        * add default values onavailable holidays report
        * add security rules for hr holydays access
        * location search  filters
        * make payments view accessible for 'billing' group
        * customize holiday, timesheet and res_partner views
        * constraint on account journal code length
    """,
    "data": [
        "views/account_payment_view.xml",
        "views/hr_holidays_view.xml",
        "views/hr_timesheet_sheet_view.xml",
        "views/location_filters.xml",
        "views/res_partner_views.xml",
        "report/available_holidays_view.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "wizard/hr_holidays_summary_department_view.xml",
        "data/sftp.xml",
        "data/data.xml",
    ],
    "installable": True,
}
