# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account For Missing Tax",
    "summary": """
        Define an account for when the tax is unassigned, for each company.""",
    "version": "12.0.1.0.1",
    "category": "Accounting & Finance",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "account",
    ],
    "excludes": [],
    "data": [
        "views/company_view.xml",
    ],
    "demo": [],
    "qweb": [],
}
