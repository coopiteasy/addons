# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleProductCompatibility(WebsiteSale):
    @http.route(
        ["/shop/cart/update"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def cart_update(
        self,
        product_id,
        add_qty=1,
        set_qty=0,
        product_custom_attribute_values=None,
        no_variant_attribute_values=None,
        express=False,
        **kwargs
    ):
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != "draft":
            request.session["sale_order_id"] = None
            sale_order = request.website.sale_get_order(force_create=True)

        warning = sale_order.check_product_compatibility(int(product_id))

        request.session["website_sale_cart_warning"] = warning

        if warning:
            return request.redirect("/shop/cart")

        return super().cart_update(
            product_id=product_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            express=express,
            **kwargs
        )

    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        warning = ""
        if "website_sale_cart_warning" in request.session:
            warning = request.session["website_sale_cart_warning"]
            del request.session["website_sale_cart_warning"]
        response = super().cart(access_token=access_token, revive=revive, **post)
        response.qcontext.update(
            {
                "website_sale_cart_warning": warning,
            }
        )
        return response
