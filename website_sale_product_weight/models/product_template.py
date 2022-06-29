# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        info = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )
        # the product_id from the function signature is overridden by the
        # internal logic of super()._get_combination_info.
        product_id = info.get("product_id", False)
        product_found = False
        if product_id:
            product = self.env["product.product"].browse(product_id)
            if product:
                product_found = True
                info.update(weight=product.weight)
                info.update(weight_uom_name=product.weight_uom_name)
        # Sane defaults from the product.template.
        if not product_found:
            info.update(weight=self.weight)
            info.update(weight_uom_name=self.weight_uom_name)
        return info
