# Copyright 2017 - Today Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime as dt

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    identical_invoice_confirmed = fields.Boolean(
        "Confirm Identical Invoice?",
        default=False,
        copy=False,
        help="You need to check this box to validate the invoice if"
        " invoices with the same partner,"
        " invoice date and totam alount already exist.",
    )
    identical_invoice_detected = fields.Boolean(
        "identical_invoice_detected", compute="_compute_identical_invoice"
    )

    @api.onchange("partner_id", "date_invoice")
    @api.multi
    def _onchange_compute_identical_invoice(self):
        self._compute_identical_invoice()

    @api.multi
    def _compute_identical_invoice(self):
        Invoice = self.env["account.invoice"]
        for invoice in self:
            duplicate_domain = [
                ("state", "not in", ["draft", "cancel"]),
                ("partner_id.supplier", "=", True),
                ("partner_id", "=", invoice.partner_id.id),
            ]
            partner_invoices = Invoice.search(duplicate_domain)

            def equal_amount(i):
                return round(i.amount_total, 2) == round(
                    invoice.amount_total, 2
                )

            def same_date(i):
                return i.date_invoice == invoice.date_invoice

            def invoiced_today(i):
                return (
                    i.date_invoice == dt.date.today()
                    and not invoice.date_invoice
                )

            duplicate_invoices = partner_invoices.filtered(
                lambda i: equal_amount(i)
                and (same_date(i) or invoiced_today(i))
            )

            invoice.identical_invoice_detected = bool(duplicate_invoices)

    @api.multi
    def invoice_validate(self):
        self._compute_identical_invoice()
        for invoice in self:
            if (
                invoice.identical_invoice_detected
                and not invoice.identical_invoice_confirmed
            ):
                raise ValidationError(
                    _(
                        "We detected invoices with the same partner, date"
                        " and total. \n\nPlease check the"
                        ' "Confirm Identical Invoice?" box to continue'
                    )
                )

        return super(AccountInvoice, self).invoice_validate()
