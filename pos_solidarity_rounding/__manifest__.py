# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Point of Sale Solidarity Rounding",
    "summary": """
        Round POS payments up for willing customers as a gesture of solidarity.""",
    "version": "12.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "point_of_sale",
    ],
    "excludes": [],
    "data": [
        "views/pos_config_views.xml",
        "views/res_partner_views.xml",
        "views/templates.xml",
    ],
    "demo": [],
    "qweb": [],
}
