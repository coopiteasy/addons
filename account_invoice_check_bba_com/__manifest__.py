# Copyright 2021 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Check Structured communication",
    "summary": """
        Check the structured communication if the supplier invoice
        communication is of type bba.
    """,
    "version": "12.0.1.0.0",
    "depends": ["account", "l10n_be_invoice_bba"],
    "author": "Coop IT Easy SCRLfs",
    "category": "Accounting & Finance",
    "website": "https://www.coopiteasy.be",
    "data": ["views/account_invoice.xml"],
    "installable": True,
}
