# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Sale Order Packaging Information",
    "summary": """
        Creates a table of packaging products on sales orders.""",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "depends": [
        "decimal_precision",
        "sale",
    ],
    "data": [
        "views/sale_order_views.xml",
        "security/ir.model.access.csv",
    ],
}
