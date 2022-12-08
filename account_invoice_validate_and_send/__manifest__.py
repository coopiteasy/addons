# © 2021 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Invoice multi validation and send",
    "category": "E-Commerce",
    "author": "Coop IT Easy SC",
    "website": "https://coopiteasy.be",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "summary": """
    This module add a wizard allowing to validate and send several
    invoice at once.
    """,
    "data": ["wizard/invoice_send_and_validate.xml"],
    "installable": True,
}
