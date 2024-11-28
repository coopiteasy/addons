# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    @api.model
    def _get_compatible_providers(
        self, *args, sale_order_id=None, website_id=None, **kwargs
    ):
        """Override of payment to exclude SEPA Direct Debit if product
        does not allow it.

        :param int sale_order_id: The sale order to be paid, if any, as
                                  a `sale.order` id
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
        # Allow only SEPA Direct Debit if at least one product must be payed
        # by SEPA Direct Debit
        only_sepa_dd_payment = any(
            order.order_line.mapped("product_id").mapped("only_sepa_dd_payment")
        )
        if not allow_sepa_dd_payment and not only_sepa_dd_payment:
            # Exclude sepa_dd
            compatible_providers = compatible_providers.filtered(
                lambda p: p.code != "custom" or p.custom_mode != "sepa_dd"
            )
        elif allow_sepa_dd_payment and only_sepa_dd_payment:
            # Get only sepa_dd
            compatible_providers = compatible_providers.filtered(
                lambda p: p.code == "custom" and p.custom_mode == "sepa_dd"
            )
        elif not allow_sepa_dd_payment and only_sepa_dd_payment:
            # Product are not compatible between each other. No payement
            # provider can be used.
            compatible_providers = self.env["payment.provider"]

        return compatible_providers
