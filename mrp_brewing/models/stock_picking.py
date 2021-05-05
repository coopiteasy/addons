# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details. # noqa
# Copyright 2019 Coop IT Easy SCRLfs

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date = fields.Datetime(
        "Creation Date",
        help="Creation Date, usually the time of the order",
        index=True,
        states={
            "done": [("readonly", False)],
            "cancel": [("readonly", False)],
        },
        track_visibility="onchange",
    )
    date_done = fields.Datetime(
        readonly=False, states={"done": [("readonly", True)]}
    )

    @api.multi
    def action_done(self):
        super(StockPicking, self).action_done()
        for picking in self:
            for move in picking.move_lines:
                move.date = picking.date_done
