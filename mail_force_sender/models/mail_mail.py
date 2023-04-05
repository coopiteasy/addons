# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models

class MailMail(models.Model):
    _inherit = "mail.mail"
    
    @api.model
    def create(self, vals):
        address = self.env["ir.config_parameter"].get_param("mail.force.sender")
        if address:
            vals["email_from"] = address
        return super().create(vals)

