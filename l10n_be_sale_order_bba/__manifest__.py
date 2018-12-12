# -*- coding: utf-8 -*-
# © 2017 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order BBA',
    'category': 'Sales',
    'author': "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be>",
    'website': 'www.coopiteasy.be',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'l10n_be_invoice_bba'
    ],
    "description": """
    This module implements the bba structured communication on the sale order.
    """,
    'data': [
        "views/sale_views.xml",
        "report/sale_order_report.xml",
    ],
    'installable': True,
}
