from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quotation_sent(self):
        # In the ecommerce flow, this method is called after the payment step,
        # the SO is then marked as sent. We override this method
        # in order to autoconfirm the ecommerce SO.
        result = super().action_quotation_sent()
        if self.website_id:
            self.action_confirm()
        # silence W8110
        return result
