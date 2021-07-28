# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    need_delivery = fields.Boolean(
        related="activity_id.need_delivery",
        string="Need delivery?",
        readonly=True,
    )
    delivery_place = fields.Char(
        related="activity_id.delivery_place",
        string="Delivery place",
        readonly=True,
    )
    delivery_time = fields.Datetime(
        related="activity_id.delivery_time",
        string="Delivery time",
        readonly=True,
    )
    pickup_place = fields.Char(
        related="activity_id.pickup_place",
        string="Pick up place",
        readonly=True,
    )
    pickup_time = fields.Datetime(
        related="activity_id.pickup_time", string="Pick up time", readonly=True
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    resource_delivery = fields.Boolean(string="Resource Delivery")
