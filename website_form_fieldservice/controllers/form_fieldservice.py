# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.website.controllers import form

LOCATION_ADDRESS = (
    "location_name",
    "location_street",
    "location_street2",
    "location_zip",
    "location_city",
    "location_state_id",
    "location_country_id",
)

REQUIRED_LOCATION_FIELDS = (
    "location_name",
    "location_street",
    "location_zip",
    "location_city",
    "location_country_id",
)


class WebsiteForm(form.WebsiteForm):
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

    @http.route("/fsm_orders/get_form_data", type="json", auth="user", website=True)
    def get_form_data(self):
        form_data = {}

        partner = request.env.user.partner_id
        form_data["beneficiaries"] = [
            {"id": b.id, "display_name": b.display_name}
            for b in self._get_same_company_beneficiaries()
        ]

        types = request.env["fsm.order.type"].sudo().search_read([], ["display_name"])
        form_data["order_types"] = [
            {"id": t["id"], "display_name": t["display_name"]} for t in types
        ]

        countries = request.env["res.country"].sudo().search_read([], ["display_name"])
        form_data["countries"] = [
            {"id": c["id"], "display_name": c["display_name"]} for c in countries
        ]

        default_country = partner.country_id or request.env.ref(
            "base.be", raise_if_not_found=False
        )
        form_data["default_country_id"] = (
            default_country.id if default_country else False
        )

        return form_data

    def _get_same_company_beneficiaries(self):
        partner = request.env.user.partner_id
        parent = partner.parent_id
        same_company_partners = (
            (parent | parent.sudo().child_ids) if parent else partner
        )
        return same_company_partners.sudo().mapped("social_beneficiary_ids")

    def _validate_fsm_order_values(self, values):
        missing = [
            field
            for field in REQUIRED_LOCATION_FIELDS
            if not str(values.get(field) or "").strip()
        ]
        beneficiary_id = values.get("social_beneficiary_partner_id")
        if (
            not beneficiary_id
            or int(beneficiary_id) not in self._get_same_company_beneficiaries().ids
        ):
            missing.append("social_beneficiary_partner_id")
        if missing:
            raise ValidationError(missing)

    def extract_data(self, model, values):
        # Pop the location address fields, otherwise they'll appear in the description
        if model.sudo().model == "fsm.order":
            self._validate_fsm_order_values(values)
            values = values.copy()
            for key in LOCATION_ADDRESS:
                values.pop(key, None)
        return super().extract_data(model, values)

    def _to_many2one(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return False

    def insert_record(self, request, model, values, custom, meta=None):
        if model.sudo().model != "fsm.order":
            return super().insert_record(request, model, values, custom, meta=meta)
        params = request.params
        location_vals = {
            "name": params.get("location_name"),
            "street": params.get("location_street"),
            "street2": params.get("location_street2"),
            "zip": params.get("location_zip"),
            "city": params.get("location_city"),
            "state_id": self._to_many2one(params.get("location_state_id")),
            "country_id": self._to_many2one(params.get("location_country_id")),
        }
        location_id = (
            request.env["fsm.location"]
            .sudo()
            .search(
                [
                    (field, "=", location_vals[field])
                    for field in (
                        "name",
                        "street",
                        "street2",
                        "zip",
                        "city",
                        "state_id",
                        "country_id",
                    )
                ],
                limit=1,
            )
        )
        if not location_id:
            location_vals["owner_id"] = request.env.user.partner_id.id
            location_vals["social_type"] = "other"
            location_id = request.env["fsm.location"].sudo().create(location_vals)
        values.update(
            {
                "location_id": location_id.id,
                "social_partner_partner_id": request.env.user.partner_id.id,
            }
        )
        return super().insert_record(request, model, values, custom, meta=meta)
