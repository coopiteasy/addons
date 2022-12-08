# Copyright 2013-2018 Open Architects Consulting SPRL.
# Copyright 2018-Coop IT Easy SC (<http://www.coopiteasy.be>)
# - Manuel Claeys Bouuaert - <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).#

{
    "name": "Removing Uniqueness Constraint for Bank Accounts",
    "version": "11.0.1.0.0",
    "author": "Coop IT Easy SC",
    "category": "Cooperative management",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
    This module removes the SQL uniqueness constraint in the Bank Account model
    res.partner.bank that requires every bank account to have a unique
    (sanitized) account number.
    """,
}
