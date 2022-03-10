# Copyright 2019 Coop IT Easy SCRLfs
# Nicolas Jamoulle, <nicolas@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Provider reference on receipt",
    "version": "12.0.1.0.0",
    "depends": ["purchase", "stock"],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "website": "https://coopiteasy.be",
    "summary": """
        Show provider reference on each line of a receipt
    """,
    "data": ["views/stock_view.xml", "reports/report_deliveryslip.xml"],
    "installable": True,
}
