# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _get_possible_variants_sorted(self, parent_combination=None):
        """This is used by `website_sale.product_variants` (list view of variants)."""
        self.ensure_one()

        return (
            super()
            ._get_possible_variants_sorted()
            .sorted(lambda product: product.qty_available > 0, reverse=True)
        )
