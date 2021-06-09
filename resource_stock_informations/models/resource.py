# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class Resource(models.Model):
    _inherit = "resource.resource"

    purchase_date = fields.Date(string="Purchase Date")
    purchase_invoice_ref = fields.Char(string="Purchase Invoice Ref")

    removed_from_stock = fields.Boolean(
        string="Removed From Stock", default=False
    )
    stock_removal_date = fields.Date(string="Stock Removal Date")
    stock_removal_reason = fields.Selection(
        string="Stock Removal Reason",
        selection=[
            ("sold", "Sold"),
            ("stolen", "Stolen"),
            ("given", "Given"),
            ("broken", "Broken"),
            ("other", "Other"),
        ],
    )
    selling_price = fields.Float(string="Selling Price")
    sale_invoice_ref = fields.Char(string="Sale Invoice Ref")

    @api.multi
    def action_remove_from_stock(self):
        self.ensure_one()
        wiz = self.env["resource.stock.removal.wizard"].create(
            {
                "resource_id": self.id,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Remove %s from Stock" % self.name,
            "view_type": "form",
            "view_mode": "form",
            "res_model": wiz._name,
            "res_id": wiz.id,
            "target": "new",
        }
