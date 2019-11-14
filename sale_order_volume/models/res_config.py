# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class SaleOrderVolumeConfiguration(models.TransientModel):
    _inherit = "sale.config.settings"

    pallet_volume = fields.Float(string="Volume of a pallet (m³)")

    @api.multi
    def set_param(self):
        self.ensure_one()

        self.env["ir.config_parameter"].set_param(
            "sale_order_volume.pallet_volume", self.pallet_volume
        )

    @api.multi
    def get_default_pallet_volume(self):
        return {
            "pallet_volume": float(
                self.env["ir.config_parameter"].get_param(
                    "sale_order_volume.pallet_volume"
                )
                or 0
            )
        }
