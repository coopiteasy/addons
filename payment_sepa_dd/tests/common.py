# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from odoo.addons.payment.tests.common import PaymentCommon


class PaymentSepaDDCommon(PaymentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.provider = cls._prepare_provider(code="sepa_dd")
        cls.iban = "BE41817358676710"

    def setUp(self):
        super().setUp()
        self.notification_data = {
            "reference": self.reference,
            "sepa_dd_accept": "sepa_dd_accept",
            "sepa_dd_iban": self.iban,
        }
