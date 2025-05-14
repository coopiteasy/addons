# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SalePartner(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            if order:
                order._check_carrier_quotation()
        return super().action_confirm()
