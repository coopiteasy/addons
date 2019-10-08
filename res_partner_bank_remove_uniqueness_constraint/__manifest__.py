# Copyright 2013-2018 Open Architects Consulting SPRL.
# Copyright 2018-Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).#

{
    "name": "Removing Uniqueness Constraint for Bank Accounts",
    "version": "'11.0.1.0.0'",
    "author": "Coop IT Easy SCRLfs",
    "category": "Cooperative management",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This module removes the SQL uniqueness constraint in the Bank Account model
    res.partner.bank that requires every bank account to have a unique
    (sanitized) account number.
    """,
    'data': [
    ]
}
