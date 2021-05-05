# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details. # noqa
# Copyright 2019 Coop IT Easy SCRLfs

from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(
        related="product_id.qty_available",
        string="Quantity On Hand",
        readonly=True,
    )
