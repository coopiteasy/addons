# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    def _set_product_template_value_ids(self):
        """This is used by `sale.variants` (regular view of product)."""
        super()._set_product_template_value_ids()
        for rec in self:
            rec.product_template_value_ids = rec.product_template_value_ids.sudo().sorted(  # noqa
                # Get product that has product_attribute_value_id (can be multiple).
                # If multiple, get the one with the highest qty_available.
                # Reverse sort on that.
                lambda ptvi: next(
                    iter(
                        self.env["product.product"]
                        .sudo()
                        .search(
                            [
                                ("product_tmpl_id", "=", rec.product_tmpl_id.id),
                                (
                                    "attribute_value_ids",
                                    "=",
                                    ptvi.product_attribute_value_id.id,
                                ),
                            ]
                        )
                        .sorted(lambda product: product.qty_available, reverse=True)
                    ),
                    self.env["product.product"],
                ).qty_available,
                reverse=True,
            )
