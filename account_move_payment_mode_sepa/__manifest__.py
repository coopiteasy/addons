# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Account Move Payment Mode SEPA",
    "version": "16.0.0.1.0",
    "category": "Banking addons",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "account_banking_sepa_direct_debit",
    ],
    "excludes": [],
    "data": ["views/report_invoice_document.xml"],
    "assets": {},
    "demo": [],
    "qweb": [],
}
