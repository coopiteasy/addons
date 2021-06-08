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
