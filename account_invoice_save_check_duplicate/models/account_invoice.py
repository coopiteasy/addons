from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        invoice = super().create(vals)
        invoice._check_duplicate_supplier_reference()

        return invoice

    def write(self, values):
        res = super().write(values)
        self._check_duplicate_supplier_reference()

        return res
