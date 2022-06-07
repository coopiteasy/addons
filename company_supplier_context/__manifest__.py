# SPDX-FileCopyrightText: 2022 Coop IT Easy SCRLfs
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Company Supplier Context",
    "summary": """
        When creating a new supplier, make it a company partner type by default.
    """,
    "version": "12.0.1.0.0",
    "category": "Sales",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": ["base"],
    "excludes": [],
    "data": ["views/partner.xml"],
    "installable": True,
}
