# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Product Contract Sale Generation",
    "summary": "Prevent loop between product_contract and contract_sale_generation",
    "version": "16.0.1.0.0",
    "category": "Contract Management",
    "website": "https://github.com/coopiteasy/addons",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "depends": [
        "product_contract",
        "contract_sale_generation",
    ],
    "data": [
        "views/sale_order.xml",
    ],
    "auto_install": True,
}
