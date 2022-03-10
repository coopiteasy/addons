from odoo import api, fields, models


class SaleOrderConfirm(models.TransientModel):
    _name = "confirm.sale.order.wizard"
    sale_order_ids = fields.Many2many(comodel_name="sale.order", string="Sale orders")

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        sale_order_ids = self.env.context["active_ids"]
        defaults["sale_order_ids"] = sale_order_ids
        return defaults

    @api.multi
    def button_confirm(self):
        self.ensure_one()
        for so in self.sale_order_ids:
            so.action_confirm()
        return True
