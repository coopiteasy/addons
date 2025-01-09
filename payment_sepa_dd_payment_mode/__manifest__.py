# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Payment SEPA Direct Debit Payment Mode",
    "summary": """
        Manage payment_mode with payment_sepa_dd
        Glue module between payment_sepa_dd and account_payment_sale.""",
    "version": "16.0.0.1.0",
    "category": "Banking addons",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["remytms"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "payment_sepa_dd",
        "account_payment_sale",
        "website_sale",
    ],
    "excludes": [],
    "data": [],
    "assets": {},
    "demo": [],
    "qweb": [],
}
