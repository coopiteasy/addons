# Copyright 2022 Coop IT Easy SC
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
        # copy to ensure original domain is not modified
        user_domain = self._fields["user_id"].domain.copy()
        if self.filter_internal_user:
            user_domain.append(("share", "=", False))
        return {"domain": {"user_id": user_domain}}
