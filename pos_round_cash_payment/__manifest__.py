# Copyright 2020 Coop IT Easy SCRLfs
#   - Robin Keunen <robin@coopiteasy.be>
#   - Houssine bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Pos Round Cash Payment",
    "version": "12.0.1.0.0",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "website": "www.coopiteasy.be",
    "description": """
        Rounds due amount to nearest 5 cents when adding a cash Payment line.
        An line is added on the invoice to record the rounding remainder.

        A Round Remainder journal must be created and assigned to the POS.

    """,
    "depends": [
        'point_of_sale',
    ],
    'data': [
        'views/pos_config.xml',
        'views/account_journal_view.xml',
        'static/src/xml/templates.xml',
    ],
    'qweb': [
        'static/src/xml/pos_round_cash_payment.xml'
    ],
    'installable': True,
}
