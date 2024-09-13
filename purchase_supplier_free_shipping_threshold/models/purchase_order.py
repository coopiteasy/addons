# Copyright 2020 - Today Coop IT Easy SC (<http://www.coopiteasy.be>)
# - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    free_shipping_threshold = fields.Monetary(
        related="partner_id.free_shipping_threshold"
    )
