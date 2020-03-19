# Copyright 2010 Camptocamp SA (http://www.camptocamp.com)
#   Joel Grand-guillaume (Camptocamp)
# Copyright 2015-2020 Coop IT Easy SCRLfs (http://coopiteasy.be)
#   Houssine Bakkali <houssine@coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnalyticActivity(models.Model):
    _name = "account.analytic.activity"
    _description = "Analytic Activity"
    _order = "code, name asc"

    name = fields.Char(string="Activity", required=True, translate=True)
    code = fields.Char(string="Reference")
    active = fields.Boolean(string="Active", default=True)
    parent_id = fields.Many2one(
        comodel_name="account.analytic.activity",
        string="Parent activity"
    )
    child_ids = fields.One2many(
        comodel_name="account.analytic.activity",
        inverse_name="parent_id",
        string="Child activities"
    )
    analytic_account_ids = fields.Many2many(
        comodel_name="account.analytic.account",
        relation="analytic_activity_analytic_account_rel",
        column1="analytic_activity_id",
        column2="analytic_account_id",
        string="Concerned Analytic Account",
        help=(
            "Analytic account that can use this activity. Leave empty "
            "to let all analytic account use this activity."
        )
    )
