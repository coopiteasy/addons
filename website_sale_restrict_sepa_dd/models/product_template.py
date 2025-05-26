# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "product.template"

    allow_sepa_dd_payment = fields.Boolean(string="Allow SEPA Direct Debit Payment")
    only_sepa_dd_payment = fields.Boolean(string="Only SEPA Direct Debit Payment")

    @api.constrains("allow_sepa_dd_payment", "only_sepa_dd_payment")
    def _check_allow_sepa_dd_payment(self):
        """Ensure that allow_sepa_dd_payment is set if
        only_sepa_dd_payment is set.
        """
        for product in self:
            if product.only_sepa_dd_payment and not product.allow_sepa_dd_payment:
                raise ValidationError(
                    _(
                        "Allow SEPA Direct Debit Payment must be enabled to "
                        "enable Only SEPA Direct Debit Payment."
                    )
                )

    @api.onchange("only_sepa_dd_payment")
    def _onchange_only_sepa_dd_payment(self):
        if self.only_sepa_dd_payment:
            self.allow_sepa_dd_payment = True

    @api.onchange("allow_sepa_dd_payment")
    def _onchange_allow_sepa_dd_payment(self):
        if not self.allow_sepa_dd_payment:
            self.only_sepa_dd_payment = False
