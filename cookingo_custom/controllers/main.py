# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDelivery(WebsiteSale):
    @http.route(["/shop/payment"], type="http", auth="public", website=True)
    def payment(self, **post):
        order = request.website.sale_get_order()
        order.add_containers()

        return super().payment(**post)
