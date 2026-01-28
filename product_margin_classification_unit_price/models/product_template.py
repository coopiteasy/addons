# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange(
        "standard_price", "taxes_id", "margin_classification_id", "list_price"
    )
    def _onchange_standard_price(self):
        (
            self.margin_state,
            self.theoretical_price,
            self.theoretical_difference,
        ) = self.env["product.product"]._get_margin_info_with_consistent_unit_price(
            self.margin_classification_id,
            self.taxes_id,
            self.name,
            self.standard_price,
            self.list_price,
            self.uom_id,
        )
