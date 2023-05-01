# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Partner Contact Type Default",
    "summary": """
        Set 'contact' as default type when creating a partner as a contact of another
        partner.""",
    "version": "16.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "base",
        "base_view_inheritance_extension",
    ],
    "data": [
        "views/res_partner_views.xml",
    ],
}
