# Copyright 2019 Coop IT Easy SCRLfs
# Nicolas Jamoulle, <nicolas@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Weight product on receipt",
    "version": "12.0.1.0.0",
    "depends": ["stock", "beesdoo_product"],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "website": "https://coopiteasy.be",
    "summary": """
        Show product weight and unit weight on each line of a receipt
    """,
    "data": ["views/stock_view.xml", "reports/report_deliveryslip.xml"],
    "installable": True,
}
