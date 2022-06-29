# Copyright 2020 - Today Coop IT Easy SC (<http://www.coopiteasy.be>)
# - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.tools.translate import _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    invoice_status = fields.Selection(
        selection_add=[
            ("partially_paid", _("Partially Paid")),
            ("paid", _("Paid")),
        ]
    )

    @api.depends(
        "state",
        "order_line.qty_invoiced",
        "order_line.qty_received",
        "order_line.product_qty",
        "invoice_ids.state",
        "invoice_ids.residual",
        "invoice_ids.amount_total",
    )
    def _get_invoiced(self):
        super()._get_invoiced()
        for order in self.filtered(lambda o: o.invoice_status in "invoiced"):
            if all(invoice.state in "paid" for invoice in order.invoice_ids):
                order.invoice_status = "paid"
                continue
            if any(invoice.state in "paid" for invoice in order.invoice_ids):
                order.invoice_status = "partially_paid"
                continue
            if all(
                invoice.state in ("open", "in_payment", "paid")
                and float_is_zero(
                    invoice.residual,
                    precision_rounding=invoice.currency_id.rounding,
                )
                for invoice in order.invoice_ids
            ):
                order.invoice_status = "paid"
            elif any(
                invoice.state in ("open", "in_payment", "paid")
                and float_compare(
                    invoice.residual,
                    0.0,
                    precision_rounding=invoice.currency_id.rounding,
                )
                == 1  # residual > 0
                and float_compare(
                    invoice.residual,
                    invoice.amount_total,
                    precision_rounding=invoice.currency_id.rounding,
                )
                == -1  # residual < amount_total
                for invoice in order.invoice_ids
            ):
                order.invoice_status = "partially_paid"
