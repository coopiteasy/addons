# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Belgium - National Number",
    "summary": """
        Belgian National Numbe.""",
    "version": "16.0.1.0.0",
    "category": "Contact",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "partner_identification",
    ],
    "data": ["data/res_partner_id_category.xml"],
    "excludes": [],
    "demo": [],
    "qweb": [],
}
