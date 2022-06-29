# Copyright 2017- Coop IT Easy SC
#   - Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Global discount on invoice",
    "version": "12.0.1.1.0",
    "author": "Coop IT Easy SC",
    "category": "Accounting",
    "license": "AGPL-3",
    "website": "https://coopiteasy.be",
    "depends": ["account", "sale"],
    "summary": """
    This module give global discount on invoice.
    It allows to set the same discount on all the invoice lines
     without been forced to go manually through them.
    """,
    "data": ["views/account_invoice_view.xml"],
    "installable": True,
}
