# Copyright 2020 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Grégoire Leeuwerck  <gregoire@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account invoice check duplicate on save",
    "summary": """
        Check that account invoice hasn't been encoded twice when creating or saving.
        This step is normally done when validating. This step doesn't replace the
        validation.
    """,
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "version": "12.0.1.0.0",
    "website": "https://coopiteasy.be",
    "category": "Accounting",
    "depends": ["account"],
}
