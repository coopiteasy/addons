# Copyright 2021+ Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        invoice_ids = super(SaleOrder, self).action_invoice_create(
            grouped=grouped, final=final
        )
        try:
            self.ensure_one()
            invoice = self.env["account.invoice"].browse(invoice_ids[0])
            invoice.origin_so_id = self
        except ValueError:
            _logger.warning(
                "Could not link invoices to sale orders %s"
                % self.mapped("name")
            )
        return invoice_ids
