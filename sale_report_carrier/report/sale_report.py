# Copyright 2022 Coop IT Easy SCRLfs
#   Carmen Bianca Bakker <carmen@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    carrier_id = fields.Many2one(
        "delivery.carrier", string="Delivery Method", readonly=True
    )

    def _select(self):
        return (
            super(SaleReport, self)._select()
            + """,
            s.carrier_id as carrier_id"""
        )

    def _group_by(self):
        return (
            super(SaleReport, self)._group_by()
            + """,
            s.carrier_id"""
        )
