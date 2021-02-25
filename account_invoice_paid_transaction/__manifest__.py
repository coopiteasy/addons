# Copyright 2021+ Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Invoice Paid Online",
    "summary": "Mark invoice as paid if an online transaction exists",
    "version": "11.0.1.0.0",
    "category": "Sales",
    "website": "https://www.coopiteasy.be",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_payment",
    ],
    "data": ["views/account_invoice.xml"],
    "demo": [],
}
