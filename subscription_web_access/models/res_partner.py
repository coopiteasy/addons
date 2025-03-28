# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_web_subscribed = fields.Boolean(
        compute="_compute_subscription_status",
        store=True,
    )

    subscriber = fields.Boolean(
        compute="_compute_subscription_status",
        store=True,
    )

    @api.depends(
        "contract_ids.contract_line_ids.state",
        "contract_ids.contract_line_ids.product_id.is_trial",
    )
    def _compute_subscription_status(self):
        for rec in self:
            rec.is_web_subscribed = False
            rec.subscriber = False
            for contract in rec.contract_ids:
                for line in contract.contract_line_ids:
                    if line.state == "in-progress" or line.state == "upcoming-close":
                        rec.is_web_subscribed = True
                        if not line.product_id.is_trial:
                            rec.subscriber = True
