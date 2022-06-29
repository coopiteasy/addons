# Copyright 2017 - Today Coop IT Easy SC (<http://www.coopiteasy.be>)
# - Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Check Identical Invoice",
    "summary": """
        Check if invoices with the same partner, invoice date
        and total amount already exist""",
    "version": "12.0.1.0.0",
    "depends": ["base", "account"],
    "author": "Coop IT Easy SC",
    "category": "Accounting & Finance",
    "website": "https://coopiteasy.be",
    "data": ["views/account_invoice.xml"],
    "installable": True,
    "license": "AGPL-3",
}
