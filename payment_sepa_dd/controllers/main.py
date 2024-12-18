# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging
import pprint

from odoo import _
from odoo.exceptions import ValidationError
from odoo.http import Controller, request, route

from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)


class PaymentSEPADD(Controller):
    @route("/payment/sepa_dd/process", type="json", auth="public")
    def sepa_dd_process_transaction(self, **data):
        """Process sepa_dd payment.
        Throws ValidationError if something fails.
        """
        access_token = data.get("access_token")
        reference = data.get("reference")
        partner_id = data.get("partner_id")

        # Check that the transaction details have not been altered
        if not payment_utils.check_access_token(access_token, reference, partner_id):
            raise ValidationError(
                _("sepa_dd payment: Received tampered payment request data.")
            )

        _logger.info(
            "Handling sepa_dd payment processing with data:\n%s", pprint.pformat(data)
        )

        tx_sudo = (
            request.env["payment.transaction"]
            .sudo()
            .search([("reference", "=", reference)])
        )

        sepa_dd_accept = data.get("sepa_dd_accept")
        if not sepa_dd_accept:
            raise ValidationError(
                _("You must accept terms to give a SEPA Direct Debit Mandate.")
            )
        sepa_dd_iban = data.get("sepa_dd_iban", "")
        if not sepa_dd_iban:
            raise ValidationError(
                _("IBAN must be provided for SEPA Direct Debit payment")
            )
        tx_sudo.sepa_dd_iban = sepa_dd_iban

        # FIXME: is order accessible here? Should it be change elsewhere ?
        # Set SEPA Direct Debit payment_mode_id
        # order = request.env["sale.order"].sudo().browse(sale_order_id).exists()
        # order.payment_mode_id = order.get_sepa_dd_payment_mode()

        tx_sudo._handle_notification_data("sepa_dd", data)
