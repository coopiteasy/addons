# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from unittest.mock import patch

from odoo.tests import tagged
from odoo.tools import mute_logger

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.tests.http_common import PaymentHttpCommon
from odoo.addons.payment_sepa_dd.tests.common import PaymentSepaDDCommon


@tagged("-at_install", "post_install")
class TestProcessingFlows(PaymentSepaDDCommon, PaymentHttpCommon):
    def test_access_token(self):
        """Test that access token are correctly generated."""
        tx = self._create_transaction(flow="direct")
        with mute_logger("odoo.addons.payment.models.payment_transaction"), patch(
            "odoo.addons.payment.utils.generate_access_token",
            new=self._generate_test_access_token,
        ):
            processing_values = tx._get_processing_values()

        with patch(
            "odoo.addons.payment.utils.generate_access_token",
            new=self._generate_test_access_token,
        ):
            self.assertTrue(
                payment_utils.check_access_token(
                    processing_values["access_token"], self.reference, self.partner.id
                )
            )
