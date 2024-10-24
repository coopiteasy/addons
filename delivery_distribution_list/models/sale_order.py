from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    distribution_carrier_id = fields.Many2one(
        "res.partner", string="Assigned carrier", readonly=True
    )
    distribution_list_id = fields.Many2one(
        "delivery.distribution.list", string="Distribution list", readonly=True
    )
