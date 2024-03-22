# © 2016 Robin Keunen, Coop IT Easy SCRL.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


def _compute_pallet_count(volume, pallet_volume):
    if not pallet_volume:
        return 0
    quotient, remainder = divmod(volume, pallet_volume)
    if remainder:
        return quotient + 1
    return quotient


class SaleOrder(models.Model):
    _inherit = "sale.order"

    volume = fields.Float(
        string="Order Volume (m³)", compute="_compute_order_volume", store=True
    )

    pallet_count = fields.Integer(
        string="Order # Pallets", compute="_compute_order_volume", store=True
    )

    @api.depends("order_line", "order_line.volume")
    def _compute_order_volume(self):

        for order in self:
            order_lines = order.order_line.filtered(
                lambda ol: ol.state not in ["cancel"]
            )

            order.volume = sum(ol.volume for ol in order_lines)
            order.pallet_count = _compute_pallet_count(
                order.volume, float(self.get_default_pallet_volume())
            )

    @api.model
    def get_default_pallet_volume(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_order_volume.pallet_volume")
            or 0
        )
