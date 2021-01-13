# Copyright 2009-2019 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    supplier_invoice_number = fields.Char(
        string="Vendor Invoice Number",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
    )

    @api.onchange("supplier_invoice_number")
    def _onchange_supplier_invoice_number(self):
        if not self.reference:
            self.reference = self.supplier_invoice_number

    @api.onchange("reference")
    def _onchange_vendor_bill_reference(self):
        if (
            self.type in ["in_invoice", "in_refund"]
            and not self.supplier_invoice_number
        ):
            self.supplier_invoice_number = self.reference
