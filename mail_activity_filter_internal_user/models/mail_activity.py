# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MailActivity(models.Model):

    _inherit = "mail.activity"

    filter_internal_user = fields.Boolean(
        string="Assign to internal user only",
        default=True,
    )

    @api.onchange("filter_internal_user")
    def onchange_filter_internal_user(self):
        """
        Change the domain on the user_id field based on the value of
        filter_internal_user.
        """
        if "user_id" in self._fields:
            filter_internal_user_domain = ("share", "=", False)
            previous_domain = self._fields["user_id"].domain
            if self.filter_internal_user:
                if filter_internal_user_domain not in previous_domain:
                    previous_domain.append(filter_internal_user_domain)
            else:
                previous_domain.remove(filter_internal_user_domain)
            return {"domain": {"user_id": previous_domain}}
