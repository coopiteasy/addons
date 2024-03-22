# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Resource Bookings Sale",
    "summary": """
        Create a link between resource bookings and sales orders.""",
    "version": "14.0.1.0.0",
    "category": "Appointments",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "sale",
        "resource_booking",
    ],
    "excludes": [],
    "data": [
        "views/resource_booking_views.xml",
        "views/resource_booking_type_views.xml",
        "views/resource_resource_views.xml",
    ],
    "demo": [],
    "qweb": [],
}