# Copyright 2010 Camptocamp SA (http://www.camptocamp.com)
#   Joel Grand-guillaume (Camptocamp)
# Copyright 2015-2020 Coop IT Easy SCRLfs (http://coopiteasy.be)
#   Houssine Bakkali <houssine@coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    analytic_activity_ids = fields.Many2many(
        comodel_name="account.analytic.activity",
        relation="analytic_activity_analytic_account_rel",
        column1="analytic_account_id",
        column2="analytic_activity_id",
        string="Related Analytic Activities",
        help=(
            "Analytic Activities that can be used with this account. "
            "Leave empty to let use all activities."
        )
    )


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    analytic_activity_id = fields.Many2one(
        comodel_name="account.analytic.activity",
        string="Activity"
    )
