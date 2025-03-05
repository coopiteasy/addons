# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import models
from odoo.tools import email_normalize


class AccountMove(models.Model):
    _inherit = "account.move"

    def create_user_for_gift(self):
        for invoice in self:
            partner_id = invoice.partner_id
            is_gift = any(
                invoice.line_ids.mapped("contract_line_id")
                .mapped("contract_id")
                .mapped("is_gift")
            )
            if not partner_id.user_id and is_gift:
                # TODO: send email to the reciever of the gift
                self.env["res.users"].with_context(
                    no_reset_password=True
                )._create_user_from_template(
                    {
                        "email": email_normalize(partner_id.email),
                        "login": email_normalize(partner_id.email),
                        "partner_id": partner_id.id,
                    }
                )
