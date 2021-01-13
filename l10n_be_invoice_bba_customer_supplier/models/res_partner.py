# Copyright 2009-2019 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    out_inv_comm_type = fields.Selection(
        selection="_selection_out_inv_comm_type",
        string="Communication Type",
        change_default=True,
        default="none",
        help="Select Default Communication Type for Outgoing Invoices.",
    )
    out_inv_comm_algorithm = fields.Selection(
        selection="_select_out_inv_comm_algorithm",
        string="Communication Algorithm",
        help="Select Algorithm to generate the "
        "Structured Communication on Outgoing Invoices.",
    )

    @api.model
    def _selection_out_inv_comm_type(self):
        res = self.env["account.invoice"]._selection_reference_type()
        return res

    @api.model
    def _select_out_inv_comm_algorithm(self):
        return [
            ("random", "Random"),
            ("date", "Date"),
            ("partner_ref", "Customer Reference"),
        ]

    @api.onchange("supplier")
    def _onchange_supplier(self):
        """ don't set 'bba' for suppliers """
        if self.supplier and not self.customer:
            if self.out_inv_comm_type == "bba":
                self.out_inv_comm_type = "none"
