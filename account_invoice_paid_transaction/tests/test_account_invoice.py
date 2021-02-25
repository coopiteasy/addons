# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class AccountInvoiceCase(TransactionCase):
    def setUp(self):
        super(AccountInvoiceCase, self).setUp()
        self.sale_order = self.browse_ref("sale.sale_order_4")

        vals = {
            "name": "Fake Acquirer",
            "provider": "manual",
        }
        self.acquirer = self.env["payment.acquirer"].create(vals)

        self.transaction = self.env["payment.transaction"].create(
            {
                "sale_order_id": self.sale_order.id,
                "amount": self.sale_order.amount_total,
                "acquirer_id": self.acquirer.id,
                "type": "server2server",
                "currency_id": self.sale_order.currency_id.id,
                "reference": self.sale_order.name,
                "partner_id": self.sale_order.partner_id.id,
            }
        )

    def test_invoice_mark_as_paid(self):
        invoice_ids = self.sale_order.action_invoice_create()
        invoice = self.env["account.invoice"].browse(invoice_ids)

        self.assertEquals(self.sale_order, invoice.origin_so_id)
        self.assertFalse(invoice.amount_paid_by_transactions)

        self.transaction.state = "done"
        self.assertEquals(
            invoice.amount_paid_by_transactions, self.sale_order.amount_total
        )
