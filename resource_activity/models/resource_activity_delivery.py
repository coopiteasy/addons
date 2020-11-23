# -*- coding: utf-8 -*-
# Copyright 2018 Coop IT Easy SCRLfs.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResourceActivityDelivery(models.Model):
    _name = "resource.activity.delivery"

    activity_id = fields.Many2one(
        "resource.activity",
        string="Activity",
        required=True,
        ondelete="cascade",
    )
    activity_description = fields.Char(
        related="activity_id.description", string="Description",
    )
    activity_type = fields.Many2one(
        "resource.activity.type",
        string="Activity type",
        related="activity_id.activity_type",
    )
    location_id = fields.Many2one(
        "resource.location",
        string="Location",
        related="activity_id.location_id",
    )
    delivery_type = fields.Selection(
        [("delivery", "Delivery"), ("pickup", "Pick up"),],
        string="Type",
        required=True,
    )
    nb_allocated_resources = fields.Integer(
        string="Allocated Resources",
        related="activity_id.nb_allocated_resources",
    )
    state = fields.Selection(related="activity_id.state", string="State",)
    date = fields.Datetime(string="Date", compute="_compute_date", store=True,)
    place = fields.Char(string="Place", compute="_compute_place",)

    @api.multi
    @api.depends("activity_id.delivery_time", "activity_id.pickup_time")
    def _compute_date(self):
        for delivery in self:
            if delivery.is_delivery():
                delivery.date = delivery.activity_id.delivery_time
            elif delivery.is_pickup():
                delivery.date = delivery.activity_id.pickup_time
            else:
                raise ValueError(_("'delivery_type' is not defined"))

    @api.multi
    @api.depends("activity_id.delivery_place", "activity_id.pickup_place")
    def _compute_place(self):
        for delivery in self:
            if delivery.is_delivery():
                delivery.place = delivery.activity_id.delivery_place
            elif delivery.is_pickup():
                delivery.place = delivery.activity_id.pickup_place
            else:
                raise ValueError(_("'delivery_type' is not defined"))

    def is_delivery(self):
        self.ensure_one()
        return self.delivery_type == "delivery"

    def is_pickup(self):
        self.ensure_one()
        return self.delivery_type == "pickup"
