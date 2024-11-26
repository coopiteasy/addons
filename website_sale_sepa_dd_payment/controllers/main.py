# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleSEPADirectDebit(WebsiteSale):
    @http.route(
        "/shop/payment", type="http", auth="public", website=True, sitemap=False
    )
    def shop_payment(self, **post):
        sepa_dd_errors = []
        sepa_dd_iban = ""
        # Set default values
        if request.env.user.partner_id.bank_ids:
            sepa_dd_iban = request.env.user.partner_id.bank_ids[0].acc_numbre
        # Process form
        if request.httprequest.method == "POST":
            order = request.website.sale_get_order()
            order.sepa_dd_iban = request.params.get("sepa-dd-iban", "")
            try:
                order.with_context(send_email=True).action_confirm()
            except ValidationError as err:
                sepa_dd_errors.append(str(err))
            else:
                return request.redirect(order.get_portal_url())

        result = super().shop_payment(**post)
        result.qcontext["sepa_dd_errors"] = sepa_dd_errors
        result.qcontext["sepa_dd_iban"] = sepa_dd_iban
        return result
