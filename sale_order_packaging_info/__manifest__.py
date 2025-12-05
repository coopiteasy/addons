# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Sale Order Packaging Information",
    "summary": "Create a table of packaging products on sales orders",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
        "security/ir.model.access.csv",
    ],
}
