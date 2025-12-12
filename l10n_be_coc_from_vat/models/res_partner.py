# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def write(self, vals):
        # compute coc registration number from vat if partner is from belgium.
        # this cannot be done with an onchange because it should also work
        # from the pos, and neither as a computed field because
        # coc_registration_number is already a computed field.
        res = super().write(vals)
        be = self.env.ref("base.be")
        for record in self:
            if (
                record.country_id != be
                or not record.vat
                or not record.vat.startswith("BE")
            ):
                continue
            company_registry_number = record.vat[2:]
            if record.coc_registration_number != company_registry_number:
                record.coc_registration_number = company_registry_number
        return res
