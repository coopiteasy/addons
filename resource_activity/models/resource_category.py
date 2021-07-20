# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from datetime import datetime


class ResourceCategory(models.Model):
    _inherit = "resource.category"

    product_ids = fields.Many2many("product.product", string="Product")


class ResourceCategoryAvailable(models.Model):
    _name = "resource.category.available"
    activity_id = fields.Many2one(
        comodel_name="resource.activity", string="Activity"
    )
    category_id = fields.Many2one(
        comodel_name="resource.category", string="Category", required=True
    )
    nb_resources = fields.Integer(string="Number of resources")

    @api.model
    def garbage_collect(self):
        """cleanup resource category available for past activities"""
        a_week_ago = datetime.now() - timedelta(days=7)
        a_week_ago_str = fields.Datetime.to_string(a_week_ago)
        self.search(
            [
                "|",
                ("activity_id", "=", False),
                ("activity_id.date_start", "<=", a_week_ago_str),
            ]
        ).unlink()
