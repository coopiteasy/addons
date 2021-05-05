# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details. # noqa
# Copyright 2019 Coop IT Easy SCRLfs

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    _order = "has_stock desc, create_date asc"

    qty_available = fields.Float(
        string="Quantity available",
        compute="_compute_qty_available",
        store=True,
    )

    has_stock = fields.Boolean(
        string="Has Stock", compute="_compute_qty_available", store=True
    )

    @api.multi
    @api.depends("quant_ids.reservation_id")
    def _compute_qty_available(self):
        for lot in self:
            quants = lot.quant_ids.filtered(
                lambda r: r.location_id.usage == "internal"
                and not r.reservation_id
            )  # noqa
            qty = sum(quants.mapped("qty"))
            lot.qty_available = qty
            lot.has_stock = qty > 0

    @api.model
    def _batch_compute_qty_available(self):
        lots = self.env["stock.production.lot"].search([])
        lots._compute_qty_available()
