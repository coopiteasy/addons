# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Resource Activity Terms",
    "version": "9.0.1.0.1",
    "depends": [
        "resource_activity",
    ],
    "author": "Coop IT Easy SCRL fs",
    "category": "Resource",
    "website": "https://www.coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
        Manage activity terms per location.
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/res_company_note_views.xml",
        "views/res_company_views.xml",
        "views/res_company_terms_views.xml",
        "views/resource_location_views.xml",
        "views/sale_order_views.xml",
        "reports/sale_order_report.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
}
