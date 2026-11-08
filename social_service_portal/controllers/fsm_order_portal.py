# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import http
from odoo.http import request
from odoo.osv.expression import AND

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    def _prepare_fsm_orders_domain(self):
        domain = super()._prepare_fsm_orders_domain()
        user = request.env.user
        is_partner = user.has_group("social_service_portal.group_portal_social_partner")
        is_volunteer = user.has_group(
            "social_service_portal.group_portal_social_volunteer"
        )
        if is_partner:
            social_domain = [
                (
                    "social_partner_partner_id",
                    "=",
                    user.partner_id.id,
                ),
            ]
        elif is_volunteer:
            person_ids = (
                request.env["fsm.person"]
                .sudo()
                .search([("partner_id", "=", user.partner_id.id)])
            )
            if not person_ids:
                return AND([domain, [(0, "=", 1)]])
            social_domain = [
                "|",
                ("person_id", "=", False),
                ("person_id", "in", person_ids.ids),
            ]
        else:
            social_domain = [(0, "=", 1)]
        return AND([domain, social_domain])

    @http.route(
        ["/my/fsm_orders", "/my/fsm_orders/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_fsm_orders(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        groupby=None,
        search=None,
        search_in="all",
        **kw,
    ):
        if not groupby:
            groupby = "stage_id"
        return super().portal_my_fsm_orders(
            page,
            date_begin,
            date_end,
            sortby,
            filterby,
            groupby,
            search,
            search_in,
            **kw,
        )
