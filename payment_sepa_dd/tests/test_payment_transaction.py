# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.payment.tests.http_common import PaymentHttpCommon
from odoo.addons.payment_sepa_dd.tests.common import PaymentSepaDDCommon


@tagged("-at_install", "post_install")
class TestPaymentTransaction(PaymentSepaDDCommon, PaymentHttpCommon):
    def test_processing_notification_data(self):
        """Test that processing transaction set transaction as pending."""
        tx = self._create_transaction("direct")
        tx._process_notification_data(self.notification_data)
        self.assertEqual(tx.state, "pending")

    def test_processing_notification_data_no_iban(self):
        tx = self._create_transaction("direct")
        del self.notification_data["sepa_dd_iban"]
        with self.assertRaises(ValidationError):
            tx._process_notification_data(self.notification_data)

    def test_processing_notification_data_wrong_iban(self):
        tx = self._create_transaction("direct")
        self.notification_data["sepa_dd_iban"] = "AAAA"
        with self.assertRaises(ValidationError):
            tx._process_notification_data(self.notification_data)

    def test_processing_notification_data_no_accept(self):
        tx = self._create_transaction("direct")
        del self.notification_data["sepa_dd_accept"]
        with self.assertRaises(ValidationError):
            tx._process_notification_data(self.notification_data)

    def test_processing_notification_mandate_creation(self):
        """Test that processing transaction set transaction as pending."""
        tx = self._create_transaction("direct")
        tx._process_notification_data(self.notification_data)
        # TODO: check that mandate exists
