# -*- coding: utf-8 -*-
{
    "name": """POS Network Printer""",
    "summary": """The time has come. Print POS orders and receipts by using "
    "network printers""",
    "category": "Point of Sale",
    "images": ['images/pos_printer_network_main.png'],
    "version": "2.0.0",

    "author": "IT-Projects LLC, Dinar Gabbasov",
    "support": "apps@it-projects.info",
    "website": "https://twitter.com/gabbasov_dinar",
    "license": "LGPL-3",

    "depends": [
        "point_of_sale",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "views/pos_printer_network_template.xml",
        "views/pos_printer_network_view.xml",
    ],
    'qweb': [
        "static/src/xml/pos_printer_network.xml",
    ],

    "installable": True,
}
