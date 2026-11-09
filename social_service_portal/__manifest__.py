# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Social Service Portal",
    "summary": "Portal for social service",
    "version": "18.0.1.0.0",
    "category": "Website/Website",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["mihien"],
    "license": "AGPL-3",
    "depends": [
        "fieldservice_portal",
        "partner_social_service",
    ],
    "data": [
        "data/fsm_stage.xml",
        "security/social_service_security.xml",
        "security/ir.model.access.csv",
        "views/fsm_order_template.xml",
        "views/fsm_order.xml",
    ],
}
