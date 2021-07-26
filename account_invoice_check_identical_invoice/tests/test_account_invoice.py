# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.tests import TransactionCase


class TestAccountInvoice(TransactionCase):
    # todo
    def test_identical_in_invoice_raises(self):
        self.assertTrue(True)

    def test_identical_out_invoice_passes(self):
        self.assertTrue(True)
