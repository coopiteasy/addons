# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import json

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def get_subscription(self, user_id):
        user = self.env["res.users"].browse(user_id)
        if not user:
            return json.dumps({"error": "user not found"})

        partner = user.partner_id
        if not partner:
            return json.dumps(
                {
                    "id": user_id,
                    "start": "",
                    "end": "",
                    "subscription": "",
                    "subscribed": False,
                }
            )

        # todo : this is the same code as in res.partner._compute_subscription_status().
        # this could be refactored either as a computed field (something like
        # ongoing_contract_line_id) or as a method (something like
        # .get_ongoing_contract_line()).
        # both should return an empty contract.line recordset
        # in case there is no ongoing contract line.
        for contract in partner.contract_ids:
            for line in contract.contract_line_ids:
                if line.state == "in-progress" or line.state == "upcoming-close":
                    return json.dumps(
                        {
                            "id": user_id,
                            "start": line.date_start,
                            "end": line.date_end,
                            "subscription": line.contract_id.name,
                            "subscribed": partner.is_web_subscribed,
                        },
                        default=str,  # needed to convert dates to strings
                    )
        return json.dumps(
            {
                "id": user_id,
                "start": "",
                "end": "",
                "subscription": "",
                "subscribed": partner.is_web_subscribed,
            }
        )
