# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        orders._check_assigned_stage()
        return orders

    def write(self, vals):
        res = super().write(vals)
        if "person_id" in vals:
            self._check_assigned_stage()
        return res

    social_beneficiary_partner_id = fields.Many2one(
        string="Beneficiary",
        comodel_name="res.partner",
        domain=[("social_type", "=", "beneficiary")],
    )

    social_partner_partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[("social_type", "=", "partner")],
    )

    def _check_assigned_stage(self):
        stage_new = self.env.ref("fieldservice.fsm_stage_new")
        stage_assigned = self.env.ref("social_service_portal.fsm_stage_assigned")
        for order in self:
            if order.person_id and order.stage_id == stage_new:
                order.stage_id = stage_assigned
            elif not order.person_id and order.stage_id == stage_assigned:
                order.stage_id = stage_new
