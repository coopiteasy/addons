# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Coop IT Easy Website Branding",
    "summary": "Replace default Odoo website branding by Coop IT Easy branding",
    "version": "16.0.2.0.0",
    "category": "Website",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "depends": [
        "web_rebrand_coopiteasy",
        "website",
    ],
    "data": [
        "templates/rebrand_coopiteasy.xml",
    ],
    "auto_install": True,
}
