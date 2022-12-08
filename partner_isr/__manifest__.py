# Copyright 2020-      Coop IT Easy SC (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner ISR",
    "version": "11.0.1.0.1",
    "depends": ["base", "sale"],
    "author": "Coop IT Easy SC",
    "category": "Sales",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
    This module adds ISR number on res partner. It also allows to match the
    account bank statements lines with the corresponding partner based on
    the isr number
    """,
    "data": [
        "data/customer_id_sequence.xml",
        "views/partner_view.xml",
        "views/account_bank_statement_view.xml",
    ],
    "installable": True,
}
