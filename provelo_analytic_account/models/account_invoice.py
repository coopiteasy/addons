# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    activity_id = fields.Many2one(
        comodel_name="resource.activity", string="Activity",
    )
    project_id = fields.Many2one(
        comodel_name="pv.project", string="Project", store=True,
    )
    location_id = fields.Many2one(related="project_id.location_id")
    department_id = fields.Many2one(related="project_id.department_id")

    allowed_financing_ids = fields.Many2many(
        comodel_name="pv.financing", compute="_compute_allowed_financing"
    )
    financing_id = fields.Many2one(
        comodel_name="pv.financing", string="Financing", required=False,
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

    @api.multi
    @api.depends("project_id")
    def _compute_allowed_financing(self):
        all_financing = self.env["pv.financing"].search([])
        for invoice in self:
            if invoice.project_id and invoice.project_id.allowed_financing_ids:
                invoice.allowed_financing_ids = (
                    invoice.project_id.allowed_financing_ids
                )
            else:
                invoice.allowed_financing_ids = all_financing
