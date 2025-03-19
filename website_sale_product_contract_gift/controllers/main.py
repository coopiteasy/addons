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
        form"""
        order = request.website.sale_get_order()
        errors = {}
        if order.is_gift:
            # disable express checkout
            if "express" in post:
                del post["express"]

            # if form is sent
            if request.httprequest.method == "POST":
                # Check form
                vals, errors = self.validate_gift_form_order_line(post)
                # Check that shipping address has an email
                if not order.partner_shipping_id.email:
                    errors["email"] = _(
                        "The receiver of the gift must have an email address defined."
                    )
                if not errors:
                    order.order_line.filtered(lambda r: r.product_id.is_gift).write(
                        vals
                    )
                    return request.redirect("/shop/confirm_order")
        result = super().checkout(**post)
        result.qcontext["errors"] = errors
        result.qcontext["gift_date"] = post.get("gift_date", order.gift_date)
        return result

    def validate_gift_form_order_line(self, data):
        """Validate the gift form, and return vals for order line"""
        errors = {}
        vals = {}
        gift_date = data.get("gift_date")
        if gift_date:
            try:
                gift_date = date.fromisoformat(data.get("gift_date", ""))
            except ValueError:
                errors["gift_date"] = _("Date is not valid.")
            vals["date_start"] = gift_date
        else:
            errors["gift_date"] = _("Date is required.")
        return vals, errors
