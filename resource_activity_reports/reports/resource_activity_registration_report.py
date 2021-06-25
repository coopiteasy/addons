# -*- coding: utf-8 -*-
# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import tools
from openerp import models, fields


class ResourceActivityRegistrationReport(models.Model):
    _name = "resource.activity.registration.report"
    _description = "Activity Registrations Report"
    _auto = False

    registration_state = fields.Selection(
        [
            ("option", "Option"),
            ("booked", "Booked"),
        ],
        string="Registration State",
        readonly=True,
    )
    activity_id = fields.Many2one(
        comodel_name="resource.activity",
        string="Activity",
        readonly=True,
    )
    activity_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("quotation", "Quotation"),
            ("sale", "Sale"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Activity State",
        readonly=True,
    )
    activity_theme_id = fields.Many2one(
        comodel_name="resource.activity.theme",
        string="Activity Theme",
        readonly=True,
    )
    activity_type_id = fields.Many2one(
        comodel_name="resource.activity.type",
        string="Activity Type",
        readonly=True,
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        readonly=True,
    )
    project_id = fields.Many2one(
        comodel_name="pv.project",
        string="Project",
        readonly=True,
    )
    location_id = fields.Many2one(
        comodel_name="resource.location", string="Location", readonly=True
    )
    date_start = fields.Datetime(string="Date Start", readonly=True)
    need_delivery = fields.Boolean(string="Need Delivery?", readonly=True)
    need_guide = fields.Boolean(string="Need Guide?", readonly=True)
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", readonly=True
    )
    product_categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        readonly=True,
    )
    resource_categ_id = fields.Many2one(
        comodel_name="resource.category",
        string="Resource Category",
        readonly=True,
    )
    nb_bikes = fields.Integer(string="Number of Bikes", readonly=True)
    nb_participants = fields.Integer(
        string="Number of Participants",
        readonly=True,
    )
    nb_participants_wo_resource = fields.Integer(
        string="Number of Participants w/o Bike",
        readonly=True,
    )
    renting_hours = fields.Float("Number of Renting Hours", readonly=True)
    renting_days = fields.Float("Number of Renting Days", readonly=True)

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        report_query = (
            """
            CREATE or REPLACE VIEW %s as (
                SELECT rar.id                                    AS id,
                       rar.resource_activity_id                  AS activity_id,
                       rar.state                                 AS registration_state,
                       a.state                                   AS activity_state,
                       a.activity_theme                          AS activity_theme_id,
                       a.activity_type                           AS activity_type_id,
                       a.location_id                             AS location_id,
                       a.date_start                              AS date_start,
                       a.need_delivery                           AS need_delivery,
                       a.need_guide                              AS need_guide,
                       rat.analytic_account                      AS analytic_account_id,
                       rat.project_id                            AS project_id,
                       pt.id                                     AS product_id,
                       pt.categ_id                               AS product_category_id,
                       rar.resource_category                     AS resource_category,
                       coalesce(rar.quantity, 0)                 AS nb_participants,
                       coalesce(rar.nb_bikes, 0)                 AS nb_bikes,
                       coalesce(rar.quantity, 0)
                           - coalesce(rar.nb_bikes, 0) AS nb_participants_wo_bikes,
                       renting_hours                             AS renting_hours, 
                       renting_days                              AS renting_days
                FROM resource_activity_registration rar
                         JOIN resource_activity a ON a.id = rar.resource_activity_id
                         JOIN resource_activity_type rat ON a.activity_type = rat.id
                         LEFT JOIN product_product pp ON rar.product_id = pp.id
                         LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE rar.state IN ('option', 'booked')
            )
        """
            % self._table
        )

        cr.execute(report_query)
