# Copyright 2021 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Warehouse",
    "version": "12.0.1.0.0",
    "depends": [
        "sale",
        "sale_stock",
    ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Warehouse",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
    Let the warehouse of the sale order be set accordingly to a default
    warehouse set on the partner.
    """,
    "data": [
        "views/res_partner.xml",
    ],
}
