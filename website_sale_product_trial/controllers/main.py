# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleProductTrial(WebsiteSale):
    @http.route(
        "/shop/payment/validate",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def shop_payment_validate(self, sale_order_id=None, **post):
        result = super().shop_payment_validate(sale_order_id=sale_order_id, **post)
        if "my/order" in result.location:
            result.location = "/shop/main/confirmation"
        return result

    @http.route(
        "/shop/main/confirmation",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def shop_main_confirmation(self):
        """General confirmation for product. Used to skip view of the
        invoice."""
        return request.render("website_sale_product_trial.main_confirmation", {})
