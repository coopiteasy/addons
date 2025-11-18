# Copyright 2025 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    not_returned = fields.Integer(default=0)
    is_container = fields.Boolean(related="product_id.is_container")

    @api.constrains("not_returned", "product_uom_qty")
    def _check_not_returned(self):
        for line in self:
            if line.not_returned != 0 and not line.product_id.is_container:
                raise ValidationError(_("'Not Returned' is only for containers."))
            elif line.not_returned < 0:
                raise ValidationError(_("'Not Returned' must be zero or higher."))
            elif line.not_returned > line.product_uom_qty:
                raise ValidationError(
                    _("'Not Returned' may not be higher than Quantity.")
                )
