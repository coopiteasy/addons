# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Picking Operations Report Huge Sale Order Text",
    "summary": """
        At the bottom of the Picking Operations report, display the sale order in huge
        text.""",
    "version": "12.0.1.0.0",
    "category": "Warehouse",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "stock",
    ],
    "excludes": [],
    "data": [
        "report/report_stockpicking_operations.xml",
    ],
    "demo": [],
    "qweb": [],
}
