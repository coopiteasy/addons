# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import date

from odoo import _, http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleIsGift(WebsiteSale):
    @http.route(
        ["/shop/address"],
        type="http",
        methods=["GET", "POST"],
        auth="public",
        website=True,
        sitemap=False,
    )
    def address(self, **kw):
        order = request.website.sale_get_order()
        # Ensure user go back to checkout after editing an address
        if order.is_gift:
            kw["callback"] = "/shop/checkout"
        return super().address(**kw)

    @http.route(
        ["/shop/checkout"], type="http", auth="public", website=True, sitemap=False
    )
    def checkout(self, **post):
        """Prevent express checkout if order is a gift and process
        formular"""
        order = request.website.sale_get_order()
        errors = {}
        if order.is_gift:
            # disable express checkout
            if "express" in post:
                del post["express"]

            # if formular is sent
            if request.httprequest.method == "POST":
                vals, errors = self.validate_gift_form_order_line(post)
                if not errors:
                    order.order_line.filtered(lambda r: r.product_id.is_gift).write(
                        vals
                    )
                    return request.redirect("/shop/confirm_order")
        result = super().checkout(**post)
        result.qcontext["errors"] = errors
        result.qcontext["date_for_gift"] = post.get("date_for_gift", order.gift_date)
        return result

    def validate_gift_form_order_line(self, data):
        """Validate the gift formular, and return vals for order line"""
        errors = {}
        vals = {}
        date_for_gift = data.get("date_for_gift")
        if date_for_gift:
            try:
                date_for_gift = date.fromisoformat(data.get("date_for_gift", ""))
            except ValueError:
                errors["date_for_gift"] = _("Date is not valid.")
            vals["date_start"] = date_for_gift
        else:
            errors["date_for_gift"] = _("Date is required.")
        return vals, errors
