# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Event Track Speaker Catering",
    "summary": """Manage Speaker's Catering""",
    "version": "16.0.1.0.0",
    "category": "Event",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": ["event_track_multi_speaker"],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "views/event_track_speaker.xml",
        "views/event_track_speaker_meal_date.xml",
        "views/menuitems.xml",
    ],
    "demo": [],
    "qweb": [],
}
