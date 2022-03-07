# Copyright 2022 Coop IT Easy SCRL fs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    total_container_price = fields.Float(
        string="Total amount spent on containers",
        digits="Product Price",
        compute="_compute_containers_deposits",
    )
    total_deposit_price = fields.Float(
        string="Total discount received from deposit products",
        digits="Product Price",
        compute="_compute_containers_deposits",
    )
    current_deposit = fields.Float(
        string="Current Container Deposit",
        digits="Product Price",
        compute="_compute_containers_deposits",
    )
    container_order_line_ids = fields.One2many(
        comodel_name="sale.order.line",
        string="Container Order Lines",
        compute="_compute_container_order_line_ids",
    )

    @api.depends("container_order_line_ids", "sale_order_ids.order_line.not_returned")
    def _compute_containers_deposits(self):
        for partner in self:
            total_container_price = 0
            total_deposit_price = 0
            for line in partner.container_order_line_ids:
                if line.product_id.is_container:
                    total_container_price += line.price_unit * (
                        line.product_uom_qty - line.not_returned
                    )
                else:
                    total_deposit_price += line.price_total
            partner.total_container_price = total_container_price
            partner.total_deposit_price = total_deposit_price
            partner.current_deposit = total_container_price + total_deposit_price

    @api.depends("sale_order_ids", "sale_order_ids.state", "sale_order_ids.order_line")
    def _compute_container_order_line_ids(self):
        # TODO: This is not declared in `@api.depends`. If this value were to
        # change, the field won't be recomputed.
        deposit_product = self.env[
            "ir.config_parameter"
        ].get_container_deposit_product_id()
        for partner in self:
            partner.container_order_line_ids = (
                self.env["sale.order.line"]
                .search(
                    [
                        ("order_id.partner_id", "=", partner.id),
                        ("order_id.state", "in", ("sale", "done")),
                        "|",
                        ("product_id.is_container", "=", True),
                        ("product_id", "=", deposit_product.id),
                    ]
                )
                .sorted()
            )
