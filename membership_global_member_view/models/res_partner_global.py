# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models, tools

from odoo.addons.membership.models import membership


class ResPartnerGlobal(models.Model):
    _name = "res.partner.global"
    _description = "Members Global"
    _auto = False

    name = fields.Char()
    display_name = fields.Char()
    company_id = fields.Many2one("res.company")
    membership_state = fields.Selection(
        membership.STATE,
    )
    membership_start = fields.Date(
        string="Membership Start Date",
    )
    membership_stop = fields.Date(
        string="Membership End Date",
    )
    membership_category_ids = fields.Many2many(
        string="Membership Categories",
        comodel_name="membership.membership_category",
        relation="membership_membership_category_res_partner_rel",
        column1="res_partner_id",
        column2="membership_membership_category_id",
    )
    active = fields.Boolean()

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    id,
                    name,
                    display_name,
                    company_id,
                    membership_state,
                    membership_start,
                    membership_stop,
                    active
                FROM res_partner
            )
            """
        )
