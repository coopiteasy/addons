# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Multiple Dates per Track",
    "version": "16.0.1.0.0",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/coopiteasy/addons",
    "category": "Event",
    "summary": "Multiple Dates per Track",
    "depends": ["website_event_track"],
    "data": [
        "security/ir.model.access.csv",
        "views/event_track.xml",
    ],
    "installable": True,
}
