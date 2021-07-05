# -*- coding: utf-8 -*-


from openerp import tools
from openerp import models, fields


class ResourceActivityReport(models.Model):
    _name = "resource.activity.report"
    _description = "Activities Analysis"
    _auto = False

    name = fields.Many2one(
        comodel_name="resource.activity", 
        string="Activity",
        required=False, 
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("quotation", "Quotation"),
            ("sale", "Sale"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        readonly=True,
    )
    active = fields.Boolean(
        string="Active",
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
    registration_state = fields.Selection(
        [
            ("booked", "Booked"),
            ("waiting", "Waiting"),
        ],
        string="Registration State",
        readonly=True,
    )
    date_start = fields.Datetime(string="Date Start", readonly=True)
    location_id = fields.Many2one(
        comodel_name="resource.location", string="Location", readonly=True
    )
    need_delivery = fields.Boolean(string="Need Delivery?", readonly=True)
    need_guide = fields.Boolean(string="Need Guide?", readonly=True)
    nb_participants = fields.Integer(string="Number of participants")
    nb_bikes = fields.Integer(
        string="Number of bikes",
        readonly=True,
    )
    nb_participants_wo_bike = fields.Integer(
        string="Participants w/o bike",
        readonly=True,
    )
    nb_participants_w_bikes = fields.Integer(
        string="Participants with bikes",
        readonly=True,
    )
    renting_hours = fields.Float("Renting Hours", readonly=True)
    renting_days = fields.Integer("Renting Days", readonly=True)
    total_taxed_amount = fields.Float("Total Amount incl. tax", readonly=True)
    total_untaxed_amount = fields.Float(
        "Total Amount excl. tax", readonly=True
    )

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        report_query = """
            CREATE or REPLACE VIEW %s as (
               WITH registration_metrics AS (
                    SELECT rar.resource_activity_id AS activity_id,
                           sum(rar.quantity)        AS nb_participants,
                           sum(rar.nb_bikes)        AS nb_bikes,
                           sum(CASE
                                   WHEN NOT (quantity = 0 AND quantity_needed != 0)
                                       THEN quantity - quantity_needed
                                   ELSE 0
                               END)                 AS nb_participants_wo_bike,
                           sum(renting_seconds)     AS renting_seconds,
                           sum(renting_hours)       AS renting_hours,
                           sum(renting_days)        as renting_days
                    FROM resource_activity_registration rar
                             join resource_activity a on rar.resource_activity_id = a.id
                    WHERE rar.state != 'cancelled' 
                    GROUP BY activity_id
                ),
                     sale_orders AS (
                         SELECT ra.id                  AS activity_id,
                                sum(so.amount_total)   AS total_taxed_amount,
                                sum(so.amount_untaxed) AS total_untaxed_amount
                         FROM resource_activity ra
                                  JOIN sale_order so ON ra.id = so.activity_id
                         GROUP BY ra.id
                     )
                SELECT a.id                                                  AS id,
                       a.id                                                  AS name,
                       a.state                                               AS state,
                       a.active                                              AS active,
                       a.activity_theme                                      AS activity_theme_id,
                       a.activity_type                                       AS activity_type_id,
                       a.location_id                                         AS location_id,
                       a.date_start                                          AS date_start,
                       a.need_delivery                                       AS need_delivery,
                       a.need_guide                                          AS need_guide,
                       a.registration_state                                  AS registration_state,
                       rat.analytic_account                                  AS analytic_account_id,
                       rat.project_id                                        AS project_id,
                       a.registrations_expected                              AS nb_participants,
                       rm.nb_bikes                                           AS nb_bikes,
                       rm.nb_participants_wo_bike                            AS nb_participants_wo_bike,
                       a.registrations_expected - rm.nb_participants_wo_bike AS nb_participants_w_bikes,
                       rm.renting_hours                                      AS renting_hours,
                       rm.renting_days                                       AS renting_days,
                       so.total_taxed_amount                                 AS total_taxed_amount,
                       so.total_untaxed_amount                               AS total_untaxed_amount
                FROM resource_activity a
                         JOIN resource_activity_type rat ON a.activity_type = rat.id
                         LEFT JOIN registration_metrics rm ON rm.activity_id = a.id
                         LEFT JOIN sale_orders so on so.activity_id = a.id
                ORDER BY id
            )""" % (
            self._table
        )
        cr.execute(report_query)
