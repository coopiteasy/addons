# © 2016 Robin Keunen, Coop IT Easy SCRL fs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    display_weight = fields.Float("Display Weight", related="product_id.display_weight")

    display_unit = fields.Many2one(
        "uom.uom", "Weight Unit", related="product_id.display_unit"
    )
