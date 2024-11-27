# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.addons.base_iban.models.res_partner_bank import validate_iban


class SaleOrder(models.Model):
    _inherit = "sale.order"

    allow_sepa_dd_payment = fields.Boolean(compute="_compute_allow_sepa_dd_payment")
    sepa_dd_iban = fields.Char()

    @api.depends("order_line", "payment_mode_id")
    def _compute_allow_sepa_dd_payment(self):
        for order in self:
            only_allowed = all(
                order.order_line.mapped("product_id").mapped("allow_sepa_dd_payment")
            )
            order.allow_sepa_dd_payment = only_allowed

    def get_sepa_dd_payment_mode(self):
        return self.env["account.payment.mode"].search(
            [("payment_method_id.code", "=", "sepa_direct_debit")],
            limit=1,
        )

    def action_confirm(self):
        sepa_dd_payment_mode = self.get_sepa_dd_payment_mode()
        for order in self:
            if order.payment_mode_id == sepa_dd_payment_mode:
                order.create_sepa_dd_mandate()
        return super().action_confirm()

    def validate_sepa_dd_iban(self):
        """Raise ValidationError if sepa_dd_iban is not correct"""
        self.ensure_one()
        validate_iban(self.sepa_dd_iban)
        sanitized_sepa_dd_iban = sanitize_account_number(self.sepa_dd_iban)
        res_partner_bank = self.env["res.partner.bank"].search(
            [("sanitized_acc_number", "=", sanitized_sepa_dd_iban)],
            limit=1,
        )
        if res_partner_bank and res_partner_bank.partner_id != self.partner_id:
            raise ValidationError(
                f"The account number {sanitized_sepa_dd_iban} does not belongs "
                f"to {self.partner_id.name}."
            )
        return res_partner_bank

    def sepa_dd_mandate_vals(self):
        self.ensure_one()
        return {
            "format": "sepa",
            "type": "recurrent",
            "scheme": "CORE",
            "recurrent_sequence_type": "recurring",
            "signature_date": datetime.datetime.now(),
            "state": "valid",
        }

    def create_sepa_dd_mandate(self):
        for order in self:
            res_partner_bank = order.validate_sepa_dd_iban()
            if not res_partner_bank:
                res_partner_bank = self.env["res.partner.bank"].create(
                    {
                        "partner_id": order.partner_id.id,
                        "acc_number": order.sepa_dd_iban,
                    }
                )
            res_partner_bank.write(
                {
                    "mandate_ids": [
                        (0, 0, order.sepa_dd_mandate_vals()),
                    ],
                }
            )
