from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    is_sepa_payment = fields.Boolean(
        compute="_compute_is_sepa_payment", store=True, readonly="True", default=False
    )

    @api.depends("payment_mode_id.payment_method_id")
    def _compute_is_sepa_payment(self):
        for move in self:
            move.is_sepa_payment = False
            if move.payment_mode_id.payment_method_id == self.env.ref(
                "account_banking_sepa_direct_debit.sepa_direct_debit"
            ):
                move.is_sepa_payment = True
