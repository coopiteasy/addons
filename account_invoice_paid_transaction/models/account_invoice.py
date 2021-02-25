# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    origin_so_id = fields.Many2one(
        comodel_name="sale.order",
        string="Origin Sale Order",
        help="Set at invoice creation from a *single* sale order.",
    )
    amount_paid_by_transactions = fields.Float(
        string="Paid by SO Transactions",
        compute="_compute_paid_by_transactions",
        store=True,
        help="Amount paid through payment transactions linked"
        " to original sale order",
    )

    @api.multi
    @api.depends(
        "origin_so_id",
        "origin_so_id.payment_tx_ids",
        "origin_so_id.payment_tx_ids.state",
    )
    def _compute_paid_by_transactions(self):
        for invoice in self:
            transactions = invoice.origin_so_id.payment_tx_ids.filtered(
                lambda p: p.state == "done"
            )
            invoice.amount_paid_by_transactions = sum(
                transactions.mapped("amount")
            )
