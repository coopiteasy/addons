# Copyright 2021 - Today Coop IT Easy SC
#     - Houssine Bakkali <houssine@coopiteasy.be>
#     - Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Report Certisys Label",
    "summary": "Add Certisys Label on account, stock and sale reports",
    "category": "Reporting",
    "version": "11.0.1.0.0",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "website": "https://coopiteasy.be",
    "depends": ["account", "stock", "sale"],
    "data": [
        "reports/invoice_template.xml",
        "reports/stock_template.xml",
        "reports/sale_template.xml",
    ],
    "installable": True,
}
