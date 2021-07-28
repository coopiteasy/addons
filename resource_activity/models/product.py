# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "registration_counter desc"

    # fixme bad naming: ids
    resource_category_id = fields.Many2many(
        "resource.category", string="Resource category"
    )
    # fixme really bad naming
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


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_guide = fields.Boolean(string="Guide")
    is_participation = fields.Boolean(string="Participation")
