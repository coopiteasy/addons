# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import http
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.http import request


class WebsiteSaleCloseController(website_sale):
    """
    Overwrite routes from website_sale controller to close the
    e-commerce when required by configuration.
    """

    def closed_ecommerce(self):
        return request.render(
            "website_sale_close.closed_ecommerce",
            {"text_closed_ecommerce": request.website.text_closed_ecommerce},
        )

    @http.route()
    def shop(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).shop(*args, **kwargs)
        return self.closed_ecommerce()

    @http.route()
    def product(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).product(*args, **kwargs)
        return self.closed_ecommerce()

    @http.route()
    def pricelist(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).pricelist(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def cart(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).cart(*args, **kwargs)
        return self.closed_ecommerce()

    @http.route()
    def cart_update(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).cart_update(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def checkout(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).checkout(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def confirm_order(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).confirm_order(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def extra_info(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).extra_info(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def payment(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).payment(*args, **kwargs)
        return self.closed_ecommerce()

    @http.route()
    def payment_validate(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).payment_validate(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def payment_confirmation(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(
                WebsiteSaleCloseController, self
            ).payment_confirmation(*args, **kwargs)
        return self.closed_ecommerce()

    @http.route()
    def print_saleorder(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).print_saleorder(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def add_product(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).add_product(
                *args, **kwargs
            )
        return self.closed_ecommerce()

    @http.route()
    def pricelist_change(self, *args, **kwargs):
        if request.website.is_ecommerce_open:
            return super(WebsiteSaleCloseController, self).pricelist_change(
                *args, **kwargs
            )
        return self.closed_ecommerce()
