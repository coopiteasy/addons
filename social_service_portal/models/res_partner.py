# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        res = super().write(vals)

        if "is_social_volunteer" in vals or "social_type" in vals:
            group = self.env.ref("social_service_portal.group_portal_social_volunteer")
            for partner in self:
                if partner.social_type == "accompagner" and partner.is_social_volunteer:
                    partner.user_ids.sudo().write({"groups_id": [(4, group.id)]})
                else:
                    partner.user_ids.sudo().write({"groups_id": [(3, group.id)]})

        if "social_type" in vals:
            group = self.env.ref("social_service_portal.group_portal_social_partner")
            for partner in self:
                if partner.social_type == "partner":
                    partner.user_ids.sudo().write({"groups_id": [(4, group.id)]})
                else:
                    partner.user_ids.sudo().write({"groups_id": [(3, group.id)]})
        return res
