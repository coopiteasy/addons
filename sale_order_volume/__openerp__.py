# -*- coding: utf-8 -*-
# © 2017 - Coop IT Easy SCRLfs. (<http://www.coopiteasy.be>)
# © 2018 - Robin Keunen <robin@coopiteasy.be>
# © 2019 Elouan Le Bars <elouan@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Volume",
    "version": "9.0.1.1.0",
    "depends": [
        'sale',
        'website_sale',
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Sale",
    "website": "www.coopiteasy.be",
    'license': 'AGPL-3',
    "description": """
        Computes the volume of products per category ordered and display it on
        - sale order page,
        - sale order report,
        - website shop cart website page.
        The corresponding number of pallets is displayed on
        - sale order page
        - website shop cart website page.
        Pallet volume is configurable.
    """,
    'data': [
        'data/res_config_data.xml',
        'views/res_config_view.xml',
        'views/sale_order.xml',
        'views/shopping_cart.xml',
        'reports/report_saleorder.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
