# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    @api.onchange("iface_tipproduct")
    def _onchange_tipproduct(self):
        if self.iface_tipproduct:
            self.tip_product_id = self.env.ref(
                "point_of_sale.product_product_tip", False
            )
        else:
            self.tip_product_id = False
