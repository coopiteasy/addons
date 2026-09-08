# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    social_beneficiary_partner_id = fields.Many2one(
        string="Beneficiary", comodel_name="res.partner"
    )

    social_partner_partner_id = fields.Many2one(
        string="Partner", comodel_name="res.partner"
    )

    location_street = fields.Char()
    location_street2 = fields.Char()
    location_zip = fields.Char(change_default=True)
    location_city = fields.Char()
    location_state_id = fields.Many2one(
        "res.country.state",
        string="State",
        ondelete="restrict",
        domain="[('country_id', '=?', location_country_id)]",
    )
    location_country_id = fields.Many2one(
        "res.country", string="Country", ondelete="restrict"
    )
    location_country_code = fields.Char(
        related="location_country_id.code", string="Country Code"
    )
