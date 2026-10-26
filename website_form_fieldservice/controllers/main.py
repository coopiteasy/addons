# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import http
from odoo.http import request

from odoo.addons.website.controllers import form


class WebsiteForm(form.WebsiteForm):
    @http.route("/fsm_orders/get_form_data", type="json", auth="user", website=True)
    def get_form_data(self):
        partner = request.env.user.partner_id
        parent = partner.parent_id
        types = request.env["fsm.order.type"].sudo().search_read([], ["display_name"])
        default_country_id = partner.country_id.id
        if not default_country_id:
            default_country_id = (
                request.env.ref("base.be", raise_if_not_found=False).id or False
            )
        return {
            "beneficiaries": [
                {"id": p.id, "display_name": p.display_name}
                for p in partner.social_beneficiary_ids + parent.social_beneficiary_ids
            ],
            "order_types": [
                {"id": t["id"], "display_name": t["display_name"]} for t in types
            ],
            "default_country_id": default_country_id,
        }

    @http.route("/fsm_orders/get_states", type="json", auth="user", website=True)
    def get_states(self, country_id):
        states = (
            request.env["res.country.state"]
            .sudo()
            .search_read([("country_id", "=", country_id)], ["display_name"])
        )
        return {
            "states": [
                {"id": s["id"], "display_name": s["display_name"]} for s in states
            ]
        }

    def extract_data(self, model, values):
        data = super().extract_data(model, values)
        if model.sudo().model == "fsm.order":
            partner_id = data["record"]["social_beneficiary_partner_id"]
            domain = [
                ("partner_id", "=", partner_id),
                ("owner_id", "=", partner_id),
            ]
            location_id = request.env["fsm.location"].sudo().search(domain, limit=1)
            if not location_id:
                vals = {
                    "partner_id": partner_id,
                    "owner_id": partner_id,
                }
                location_id = request.env["fsm.location"].sudo().create(vals)
            data["record"]["location_id"] = location_id.id
            data["record"]["social_partner_partner_id"] = request.env.user.partner_id.id
        return data
