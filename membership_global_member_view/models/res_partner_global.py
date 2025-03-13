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
    company_id = fields.Many2one("res.company")
    membership_state = fields.Selection(
        membership.STATE,
        help="It indicates the membership state.\n"
        "-Non Member: A partner who has not applied for any membership.\n"
        "-Cancelled Member: A member who has cancelled his membership.\n"
        "-Old Member: A member whose membership date has expired.\n"
        "-Waiting Member: A member who has applied for the membership "
        "and whose invoice is going to be created.\n"
        "-Invoiced Member: A member whose invoice has been created.\n"
        "-Paying member: A member who has paid the membership fee.",
    )
    membership_start = fields.Date(
        string="Membership Start Date",
        help="Date from which membership becomes active.",
    )
    membership_stop = fields.Date(
        string="Membership End Date",
        help="Date until which membership remains active.",
    )
    membership_category_ids = fields.Many2many(
        string="Membership Categories",
        comodel_name="membership.membership_category",
        relation="membership_membership_category_res_partner_rel",
        column1="res_partner_id",
        column2="membership_membership_category_id",
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    id,
                    name,
                    company_id,
                    membership_state,
                    membership_start,
                    membership_stop
                FROM res_partner
            )
            """
        )
