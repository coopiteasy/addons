# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from odoo import http
from odoo.http import request
from odoo.tools import format_amount
from odoo.tools.misc import format_date
from odoo.tools.safe_eval import datetime, safe_eval

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerWalletAmountPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "wallet_balance_formated" in counters:
            partner = request.env["res.users"].browse(request.uid).partner_id
            values["wallet_balance_formated"] = format_amount(
                request.env, partner.customer_wallet_balance, partner.currency_id
            )
        return values

    @http.route(
        ["/my/wallet", "/my/wallet/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_wallet(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw
    ):
        # Note: Pager not implemented for the time being
        partner = request.env["res.users"].browse(request.uid).partner_id

        wallet_lines = safe_eval(partner.customer_wallet_data, {"datetime": datetime})
        wallet_lines.sort(key=lambda x: (x["datetime"], x["create_date"]), reverse=True)
        for wallet_line in wallet_lines:
            wallet_line["datetime_formated"] = format_date(
                request.env, wallet_line["datetime"]
            )
            wallet_line["amount_formated"] = format_amount(
                request.env, wallet_line["amount"], partner.currency_id
            )
            wallet_line["balance_formated"] = format_amount(
                request.env, wallet_line["balance"], partner.currency_id
            )

        values = {"page_name": "wallet", "wallet_lines": wallet_lines}
        return request.render("customer_wallet_portal.portal_my_wallet", values)
