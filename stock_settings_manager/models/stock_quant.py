# Copyright 2023 Akretion (http://www.akretion.com).
# @author Olivier Nibart <olivier.nibart@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _apply_inventory(self):
        """As we don't want the stock manager to be able to write to locations
        BUT we want him to be able to apply inventories, which writes
        the last_inventory_date to the quant's location we have to do something.
        The 'view' way of doing it is complicated as odoo have 2 views related
        to locations, and not that secure.
        That's why this way has been choosen."""
        if not self.user_has_groups("stock.group_stock_manager"):
            raise UserError(
                _("Only a stock manager can validate an inventory adjustment.")
            )
        return super(StockQuant, self.sudo())._apply_inventory()
