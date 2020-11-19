from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def write(self, vals):
        # vendor bills
        if (
            not self.date
            and "date" not in vals
            and self.type in ("in_invoice", "in_refund")
        ):

            vals["date"] = fields.Date.context_today(self)

        return super(AccountInvoice, self).write(vals)
