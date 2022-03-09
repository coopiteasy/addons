# Copyright 2020 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine Bakkali  <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Import Belgian Bank Data",
    "summary": """
    This module imports Belgian banks with their name and BIC code.
    """,
    "version": "12.0.1.0.0",
    "depends": ["base", "base_iban"],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "category": "Banking addons",
    "website": "https://coopiteasy.be",
    "data": ["data/bank_data.xml"],
    "installable": True,
}
