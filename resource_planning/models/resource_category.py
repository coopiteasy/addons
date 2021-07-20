# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ResourceCategory(models.Model):
    _name = "resource.category"
    _inherit = "mail.thread"

    name = fields.Char(
        string="Category name",
        required=True,
        translate=True,
    )
    resources = fields.One2many(
        "resource.resource", "category_id", string="Resources"
    )
    is_accessory = fields.Boolean(string="Is Accessory")

    active = fields.Boolean(
        "Active", default=True, track_visibility="onchange"
    )

    @api.model
    def get_available_categories(self, date_start, date_end, location):
        allocated_resources = (
            self.env["resource.allocation"]
            .get_allocations(date_start, date_end, location)
            .mapped("resource_id")
        )

        resource_by_category = self.env["resource.resource"].read_group(
            domain=[
                ("category_id", "!=", False),
                ("id", "not in", allocated_resources.ids),
                ("state", "=", "available"),
                ("location", "=", location.id),
            ],
            fields=["category_id"],
            groupby=["category_id"],
        )
        if resource_by_category:
            resource_by_category_dict = {
                cat["category_id"][0]: int(cat["category_id_count"])
                for cat in resource_by_category
            }
        else:
            resource_by_category_dict = {}

        return resource_by_category_dict
