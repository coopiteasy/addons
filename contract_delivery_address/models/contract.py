# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery Address",
        compute="_compute_partner_shipping_id",
        store=True,
        readonly=False,
        required=True,
        precompute=True,
    )

    @api.depends("partner_id.child_ids")
    def _compute_partner_shipping_id(self):
        for contract in self:
            contract.partner_shipping_id = (
                contract.partner_id.address_get(["delivery"])["delivery"]
                if contract.partner_id
                else False
            )
