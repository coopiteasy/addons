# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    financing_id = fields.Many2one(
        comodel_name="pv.financing", string="Financing", required=False
    )
    project_id = fields.Many2one(
        comodel_name="pv.project", string="Project", store=True,
    )
    location_id = fields.Many2one(related="project_id.location_id")
    department_id = fields.Many2one(related="project_id.department_id")
    activity_id = fields.Many2one(
        comodel_name="resource.activity", string="Activity",
    )

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice, self).create(vals)
        sale_order = self.env["sale.order"].search(
            [("name", "=", invoice.origin)]
        )
        if sale_order and sale_order.activity_id:
            activity = sale_order.activity_id
            invoice.activity_id = activity
            invoice.project_id = activity.activity_type.project_id
        return invoice
