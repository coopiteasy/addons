# © 2017 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Picking Auto Send Email",
    "category": "Delivery",
    "author": "Coop IT Easy SC",
    "website": "https://coopiteasy.be",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock", "delivery", "account"],
    "summary": """
    This module allows to send confirmation email and invoice automatically
    once the picking is done according the chosen preference.
    """,
    "data": [
        "views/delivery_carrier_view.xml",
    ],
    "installable": True,
}
