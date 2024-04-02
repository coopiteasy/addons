# Copyright 2019 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import os

from odoo import models, api, _, fields
from odoo.exceptions import ValidationError
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = "res.partner"

    email = fields.Char(copy=False)

    @api.multi
    @api.constrains("email")
    def _check_email(self):
        if (
            config["test_enable"] or os.environ.get("TESTS")
        ) and not self.env.context.get("test_partner_email_unique"):
            return

        for partner in self:
            domain = [
                ("id", "!=", partner.id),
                ("email", "=", partner.email),
                ("email", "!=", False),
            ]
            other_partners = self.search(domain)

            # active_test is False when called from
            # base.partner.merge.automatic.wizard
            if other_partners and self.env.context.get("active_test", True):
                raise ValidationError(
                    _("This email is already set to partner '%s'")
                    % other_partners[0].display_name
                )
