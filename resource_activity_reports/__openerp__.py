# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource activity Reports",
    "version": "9.0.1.0.0",
    "depends": [
        "provelo_analytic_account",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Resource",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
        Reports for resource activities
    """,
    "data": [
        "security/ir.model.access.csv",
        "reports/resource_activity_report_view.xml",
        "reports/resource_activity_registration_report_view.xml",
    ],
    "installable": True,
}
