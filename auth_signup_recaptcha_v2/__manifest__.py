# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Signup reCAPTCHA v2",
    "summary": "Add reCAPTCHA v2 to sign-up form",
    "version": "12.0.1.0.0",
    "category": "Tools",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "depends": [
        "auth_signup",
        "portal_recaptcha",
    ],
    "data": ["views/auth_signup_login_templates.xml"],
}
