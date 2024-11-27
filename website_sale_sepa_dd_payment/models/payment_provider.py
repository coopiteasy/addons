# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    custom_mode = fields.Selection(selection_add=[("sepa_dd", "SEPA Direct Debit")])

    @api.model
    def _get_compatible_providers(
        self, *args, sale_order_id=None, website_id=None, **kwargs
    ):
        """Override of payment to exclude onsite providers if the delivery doesn't match.

        :param int sale_order_id: The sale order to be paid, if any, as a `sale.order` id
        :param int website_id: The provided website, as a `website` id
        :return: The compatible providers
        :rtype: recordset of `payment.provider`
        """
        compatible_providers = super()._get_compatible_providers(
            *args, sale_order_id=sale_order_id, website_id=website_id, **kwargs
        )
        order = self.env["sale.order"].browse(sale_order_id).exists()
        # Allow SEPA Direct Debit only if all products allow SEPA DD payment
        allow_sepa_dd_payment = all(
            order.order_line.mapped("product_id").mapped("allow_sepa_dd_payment")
        )
        if not allow_sepa_dd_payment:
            compatible_providers = compatible_providers.filtered(
                lambda p: p.code != "custom" or p.custom_mode != "sepa_dd"
            )

        return compatible_providers
