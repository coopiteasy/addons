# © 2016 Houssine BAKKALI, Coop IT Easy SCRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase order line auto import",
    "summary": """
        This module allows to create automatically line with the product and minimal quantities
        when selecting the partner. The user can then delete the line that he doesn't want and
        update the quantity for each product on the line.
    """,
    "author": "Houssine BAKKALI, Coop IT Easy SCRL",
    "category": "Purchase Management",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["purchase",],
    "data": ["views/purchase_order_view.xml",],
}
