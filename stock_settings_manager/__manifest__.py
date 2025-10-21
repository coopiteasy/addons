# Copyright 2023 Akretion (http://www.akretion.com).
# @author Olivier Nibart <olivier.nibart@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -----------------------------
# NOTE : this module should eventually be replaced by 2 others :
# - product manager : adding a product manager right with limited
#   rights regarding the stock management
# - a module that defines a right to make inventory, but which
#   needs to patch odoo's core o allow that.
#
# Not patching the odoo's core is the main motivation for having
# done this Stock Settings Manager module.
# -----------------------------

{
    "name": "Stock Settings Manager",
    "summary": """Add an Inventory/Settings Manager Group that is allowed
    to actually set the parameters of the inventory, including barcodes
    settings, and downgrade the Inventory/Administrator Group to allow it
    to only manage products and do inventory adjustements.""",
    "version": "16.0.1.0.0",
    "author": "Akretion",  # pylint: disable=manifest-required-author
    "website": "https://github.com/coopiteasy/addons",
    "license": "AGPL-3",
    "category": "Inventory/Inventory",
    "depends": [
        "product",
        "stock",
        "barcodes",
        "uom",
    ],
    "data": [
        "security/stock_security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
}
