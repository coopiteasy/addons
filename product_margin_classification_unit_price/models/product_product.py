# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models
from odoo.tools.float_utils import float_compare


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends_context("company")
    @api.depends(
        "standard_price",
        "lst_price",
        "margin_classification_id",
        "margin_classification_id.markup",
        "margin_classification_id.price_round",
        "margin_classification_id.price_surcharge",
        "product_tmpl_id.taxes_id",
        "product_tmpl_id.list_price",
    )
    def _compute_theoretical_multi(self):
        for product in self:
            product = product.with_company(product.company_id)
            (
                product.margin_state,
                product.theoretical_price,
                product.theoretical_difference,
            ) = self._get_margin_info_with_consistent_unit_price(
                product.margin_classification_id,
                product.taxes_id,
                product.name,
                product.standard_price,
                product.lst_price,
                product.uom_id,
            )

    @api.model
    def _get_margin_info_with_consistent_unit_price(
        self,
        classification,
        sale_taxes,
        product_name,
        standard_price,
        sale_price,
        uom_id,
    ):
        uom_quantity = uom_id.factor_inv
        unit_standard_price = standard_price / uom_quantity
        unit_sale_price = sale_price / uom_quantity
        (
            margin_state,
            unit_theoretical_price,
            unit_difference,
        ) = self._get_margin_info(
            classification,
            sale_taxes,
            product_name,
            unit_standard_price,
            unit_sale_price,
        )

        # in the above method call, margin state is computed comparing the
        # unit price and the unit_standard_price. The comparison is made a
        # with a precision for product price in the DB (often 2 decimals).
        # However, given the same precision, the state might be different when
        # comparing "box" sales price and "box" standard price. Often, the
        # state could be correct when comparing unit prices but not correct
        # when comparing "box prices".
        # In this case, the theoretical price could change with no visibility
        # for the user, and no way to update the price. Therefore, we recompute
        # the state based on the "box prices"
        theoretical_price = unit_theoretical_price * uom_quantity
        difference = sale_price - theoretical_price
        compare = float_compare(
            difference,
            0,
            precision_digits=self.env["decimal.precision"].precision_get(
                "Product Price"
            ),
        )
        if compare < 0:
            margin_state = "too_cheap"
        elif compare > 0:
            margin_state = "too_expensive"
        else:
            margin_state = "correct"
        return (margin_state, theoretical_price, difference)
