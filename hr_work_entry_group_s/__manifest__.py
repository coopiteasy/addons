# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Work Entry Group S",
    "summary": "Export the work entries of employees in the SAIAU format",
    "version": "18.0.1.0.0",
    "category": "Human Resources/Employees",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["mihien"],
    "license": "AGPL-3",
    "depends": [
        "hr_work_entry_contract",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_contract_views.xml",
        "views/res_company.xml",
        "wizard/group_s_report_wizard.xml",
    ],
}
