# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from odoo import fields, models
from odoo.fields import Date
from odoo.tools import email_normalize


class ContractContract(models.Model):
    _inherit = "contract.contract"

    is_gift = fields.Boolean()

    def _cron_recurring_create(self, date_ref=False, create_type="invoice"):
        res = super()._cron_recurring_create(date_ref=False, create_type=create_type)
        for contract in (
            self.env["contract.line"]
            .search([])
            # we look at the line date rather than the contract in case
            # line_recurrence is true. In this case, contract date would not
            # equal line date.
            .filtered(
                lambda l: l.contract_id.is_gift and (l.date_start == Date.today())
            )
            .mapped("contract_id")
        ):
            if not contract.partner_id.user_ids:
                user_with_same_login = self.env["res.users"].search(
                    [("login", "=", email_normalize(contract.partner_id.email))]
                )
                if not user_with_same_login:
                    user = (
                        self.env["res.users"]
                        .with_context(no_reset_password=True)
                        ._create_user_from_template(
                            {
                                "email": email_normalize(contract.partner_id.email),
                                "login": email_normalize(contract.partner_id.email),
                                "partner_id": contract.partner_id.id,
                            }
                        )
                    )
                    user.with_context(create_user=True).action_reset_password()
        return res
