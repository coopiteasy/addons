# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError

from collections import defaultdict


class ResourceCategory(models.Model):
    _inherit = "resource.category"

    product_ids = fields.Many2many("product.product", string="Product")


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "registration_counter desc"

    resource_category_id = fields.Many2many(
        "resource.category", string="Resource category"
    )
    resource_activity_id = fields.Many2many(
        "resource.activity.type", string="Activity type"
    )
    registration_counter = fields.Integer(
        string="Registration counter",
        default=0,
    )

    @api.model
    def compute_registration_counter(self):
        registrations = self.env["resource.activity.registration"].search(
            [("state", "=", "booked")]
        )
        # could be optimized with sql but
        # early optimisation is the root of all evil

        for registration in registrations.filtered(lambda r: r.sale_order_id):
            product_id = registration.product_id
            if product_id:
                product_id.registration_counter += 1


class ResourceLocation(models.Model):
    _inherit = "resource.location"

    guides = fields.One2many(
        "res.partner",
        "resource_location_guide",
        domain=[("is_guide", "=", True)],
        string="Guides",
    )
    trainers = fields.One2many(
        "res.partner",
        "resource_location_trainer",
        domain=[("is_trainer", "=", True)],
        string="Trainers",
    )
    opening_hours_ids = fields.Many2many(
        "activity.opening.hours", string="Opening Hours"
    )
    terms_ids = fields.One2many("resource.location.terms", "location_id")


class ResourceLocationTerms(models.Model):
    _name = "resource.location.terms"
    _description = "Resource Location Terms"

    _sql_constraints = [
        (
            "resource_location_terms_location_activity_terms_note_uq",  # Constraint unique identifier
            "UNIQUE (location_id,activity_type_id)",  # Constraint SQL syntax
            "Location, and Activity Type must be unique.",
        ),  # Message
    ]

    location_id = fields.Many2one(
        "resource.location",
        string="Location",
    )
    activity_type_id = fields.Many2one(
        "resource.activity.type", string="Activity Type", required=True
    )
    terms_id = fields.Many2one(
        "res.company.terms",
        string="Terms and Conditions",
        help="Terms and Conditions related to this location",
    )
    note_id = fields.Many2one(
        "res.company.note",
        string="Sale note",
        help="Sale note related to this location",
    )
    bike_number_display = fields.Selection(
        selection=[
            ("list", "List of Bicycles"),
            ("type", "Number of Bicycles by type"),
        ],
        string="Bike Number Display",
    )


class ResourceAllocation(models.Model):
    _inherit = "resource.allocation"

    activity_registration_id = fields.Many2one(
        "resource.activity.registration",
        string="Activity registration",
        readonly=True,
    )
    activity_id = fields.Many2one(
        related="activity_registration_id.resource_activity_id",
        string="Activity",
        readonly=True,
    )
