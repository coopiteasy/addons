# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "SEPA Direct Debit Payment",
    "summary": "Pay via SEPA Direct Debit",
    "version": "16.0.1.0.0",
    "category": "Accounting/Payment Providers",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "payment",
        "account_payment",
        "account_banking_sepa_direct_debit",
    ],
    "data": [
        "views/payment_provider_views.xml",
        "views/templates.xml",
        "data/payment_provider_data.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "payment_sepa_dd/static/src/js/payment_form.js",
            "payment_sepa_dd/static/src/js/post_processing.js",
        ],
    },
}
