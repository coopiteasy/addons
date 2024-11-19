# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    def sale_get_order(self, force_create=False, update_pricelist=False):
        """Return the default order or the order from"""
        if "sepa_debit_subscription_data" in request.session:
            sds_data = request.session["sepa_debit_subscription_data"]
            payment_mode = request.env.ref(
                "account_banking_sepa_direct_debit.sepa_direct_debit"
            )
            product = request.env["product.product"].browse(sds_data.get("product_id"))
            order = (
                request.env["sale.order"]
                .sudo()
                .new(
                    {
                        "partner_id": request.env.user.partner_id.id,
                        "order_line": [
                            (
                                0,
                                0,
                                {
                                    "product_id": product.id,
                                    "product_uom_qty": 1,
                                },
                            ),
                        ],
                        "payment_mode_id": payment_mode.id,
                    }
                )
            )
            return order
        else:
            return super().sale_get_order(
                force_create=force_create,
                update_pricelist=update_pricelist,
            )
