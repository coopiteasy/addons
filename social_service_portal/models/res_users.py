# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            if user.partner_id.social_type == "partner":
                group = self.env.ref(
                    "social_service_portal.group_portal_social_partner"
                )
                user.sudo().write({"groups_id": [(4, group.id)]})
            elif (
                user.partner_id.is_social_volunteer
                and user.partner_id.social_type == "accompagner"
            ):
                group = self.env.ref(
                    "social_service_portal.group_portal_social_volunteer"
                )
                user.sudo().write({"groups_id": [(4, group.id)]})
        return users
