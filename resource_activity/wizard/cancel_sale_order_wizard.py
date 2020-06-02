# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError, UserError


class CancelSaleOrderWizard(models.TransientModel):
    _name = "cancel.sale.order.wizard"

    @api.multi
    def cancel_sale_order(self):
        activity = self.env["resource.activity"].browse(
            self._context.get("active_ids")
        )[0]
        for sale_order in activity.sale_orders:
            sale_order.with_context(activity_action=True).action_cancel()

        return {"type": "ir.actions.act_window_close"}
