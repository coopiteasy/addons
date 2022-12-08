# Copyright 2021+ Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Invoice Paid Online",
    "summary": "Mark invoice as paid if an online transaction exists",
    "version": "11.0.1.0.0",
    "category": "Sales",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_payment",
    ],
    "data": ["views/account_invoice.xml", "report/report_invoice.xml"],
    "demo": [],
}
