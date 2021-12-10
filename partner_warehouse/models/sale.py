from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        Update the warehouse_id when a warehouse is set on a partner_id
        """
        if self.partner_id and self.partner_id.warehouse_id:
            self.warehouse_id = self.partner_id.warehouse_id
        else:
            self.warehouse_id = self._default_warehouse_id()
        super(SaleOrder, self).onchange_partner_id()
