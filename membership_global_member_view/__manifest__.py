# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Membership Global Member View",
    "summary": """Global view of the members, for all companies and without
        seeing personnal data.""",
    "version": "16.0.1.0.0",
    "category": "Membership",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "depends": ["membership", "membership_extension"],
    "data": [
        "security/groups.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/menuitems.xml",
    ],
    "demo": [],
}
