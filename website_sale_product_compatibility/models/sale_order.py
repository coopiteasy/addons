# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_product_compatibility(self, product_id):
        """Override this function to detect incompatibility between
        products.

        Warning: self.ensure_one()

        If an empty string is returned then the product_id is compatible
        and will be added to the sale order. If a warning string is
        returned then the product is considered not compatible with the
        order and the product will not be added to the order.

        By default this method always return no warning message.

        :product_id: The id of the product to check compatibility.
        :rtype: str
        :return: warning message to be shown on the web interface.
        """
        self.ensure_one()
        return ""

    def _cart_update(self, product_id, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Prevent incompatible product to be added to the cart."""
        self.ensure_one()
        warning = self.check_product_compatibility(product_id)
        if warning:
            add_qty = None
            set_qty = 0
        values = super()._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            **kwargs,
        )
        values["warning"] = warning
        return values
