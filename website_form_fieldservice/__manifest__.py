# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Website Form Fieldservice",
    "summary": "Provide a form for field service orders on the website",
    "version": "18.0.1.0.0",
    "category": "Website/Website",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["mihien"],
    "license": "AGPL-3",
    "depends": ["website", "fieldservice", "partner_social_service"],
    "data": [
        "data/ir_model_data.xml",
        "views/fsm_order.xml",
    ],
    "assets": {
        "website.assets_wysiwyg": [
            "website_form_fieldservice/static/src/js/website_fsm_order_editor.esm.js",
        ],
        "web.assets_frontend": [
            "website_form_fieldservice/static/src/js/fsm_order_form.esm.js",
        ],
    },
}
