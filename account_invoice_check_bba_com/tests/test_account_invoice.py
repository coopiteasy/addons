# Copyright 2021 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestAccountInvoiceCheckBBA(TransactionCase):
    def setUp(self):
        super(TestAccountInvoiceCheckBBA, self).setUp()
        # From "l10n_generic_coa" that seams to be installed when
        # installing this module
        self.invoice_0 = self.env.ref("l10n_generic_coa.demo_invoice_0")
        # Configure company
        self.invoice_0.company_id.invoice_reference_type = "structured"

    def test_check_bba(self):
        """
        Check to validate a invoice with wrong bba reference.
        """
        with self.assertRaises(ValidationError):
            self.invoice_0.reference = "aaabbbcccddd"
            self.invoice_0.invoice_validate()

        with self.assertRaises(ValidationError):
            self.invoice_0.reference = "+++333/4444/55555+++"
            self.invoice_0.invoice_validate()
