# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Demain Purchase Quick",
    "summary": "Add minimum quantity and purchase UoM fields to purchase "
    "order products quick add view",
    "version": "12.0.1.0.0",
    "category": "Purchase",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "purchase_quick",
        "product_main_supplier",
    ],
    "data": [
        "views/product_view.xml",
    ],
}
