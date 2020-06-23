from odoo import api, models


class InvoiceLineUpdate(models.TransientModel):
    _name = "invoice.line.update"
    _description = "Incoice line update"

    def unlink_attachment(self, report_name, invoice):
        attachment = self.env.ref(report_name).retrieve_attachment(invoice)
        if attachment:
            attachment.unlink()

    def set_to_draft(self, invoice):
        invoice.write({"state": "draft", "date": False})
        self.unlink_attachment("account.account_invoices", invoice)
        self.unlink_attachment(
            "l10n_ch_payment_slip.one_slip_per_page_from_invoice", invoice
        )

    @api.multi
    def update_invoice(self):
        invoice_ids = self.env.context.get("active_ids")

        for invoice in self.env["account.invoice"].browse(invoice_ids):
            original_state = invoice.state
            if invoice.state == "open":
                invoice.action_cancel()
                self.set_to_draft(invoice)
            elif invoice.state == "cancel":
                self.set_to_draft(invoice)

            for line in invoice.invoice_line_ids:
                price_unit = line.price_unit
                quantity = line.quantity
                line._onchange_product_id()
                line.write({"price_unit": price_unit, "quantity": quantity})
                line._compute_price()

            invoice._onchange_invoice_line_ids()
            invoice._compute_amount()
            if original_state == "open":
                invoice.action_invoice_open()
            elif original_state == "cancel":
                invoice.action_invoice_cancel()

        return True
