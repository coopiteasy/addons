import json
from openerp import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('payment_move_line_ids.amount_residual')
    def _get_payment_info_dict(self):
        # All data on earlier parments is stored as JSON in a text field
        # This function casts it back to a dictionary
        res = self.payments_widget
        d = json.loads(res)
        return d
