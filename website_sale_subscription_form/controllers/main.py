# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

SEPA_DEBIT_SUB_DATA = "sepa_debit_subscription_data"


class SubscriptionForm(http.Controller):
    @http.route(
        [
            "/sepa-debit-subscription",
            "/sepa-debit-subscription/product/<int:pid>",
        ],
        auth="public",
        website=True,
        sitemap=False,
    )
    def sepa_debit_subscriptions(self, pid=None):
        """Show list of available subscription"""
        if SEPA_DEBIT_SUB_DATA in request.session:
            del request.session[SEPA_DEBIT_SUB_DATA]
        products = request.env["product.product"].search(
            [("is_contract", "=", True), ("website_published", "=", True)]
        )
        product = request.env["product.product"].browse(pid).exists()
        if product and product in products:
            request.session[SEPA_DEBIT_SUB_DATA] = {
                "product_id": product.id,
            }
            return request.redirect("/web/login?redirect=/shop/checkout")
        values = {
            "products": products,
        }
        return request.render(
            "website_sale_subscription_form.sepa_debit_subscriptions", values
        )


class WebsiteSaleSubscription(WebsiteSale):
    @http.route(
        [
            "/shop",
            "/shop/page/<int:page>",
            '/shop/category/<model("product.public.category"):category>',
            '/shop/category/<model("product.public.category"):category>/page/<int:page>',
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=WebsiteSale.sitemap_shop,
    )
    def shop(
        self,
        page=0,
        category=None,
        search="",
        min_price=0.0,
        max_price=0.0,
        ppg=False,
        **post
    ):
        if SEPA_DEBIT_SUB_DATA in request.session:
            del request.session[SEPA_DEBIT_SUB_DATA]
        return super().shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post,
        )

    @http.route(
        ["/shop/checkout"], type="http", auth="public", website=True, sitemap=False
    )
    def checkout(self, **post):
        result = super().checkout(**post)
        if "sepa_debit_subscription_data" in request.session:
            if result.template == "website_sale.checkout":
                result.qcontext["only_services"] = False
        return result

    @http.route(
        "/shop/payment", type="http", auth="public", website=True, sitemap=False
    )
    def shop_payment(self, **post):
        if request.httprequest.method == "POST":
            # TODO: record IBAN and SEPA mandate
            order = request.website.sale_get_order()
            # FIXME: save order before ? or use dedicated existing
            # route ?
            order.with_context(send_email=True).action_confirm()
            return request.redirect(order.get_portal_url())
        return super().shop_payment(**post)
