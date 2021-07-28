# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models
from openerp.fields import Datetime
from openerp.exceptions import ValidationError
from openerp.addons.resource_activity.models.resource_activity import OrderLine
from datetime import timedelta


class ResourceActivity(models.Model):
    _inherit = "resource.activity"
    need_delivery = fields.Boolean(string="Need delivery?")

    delivery_product_id = fields.Many2one(
        "product.product",
        string="Product delivery",
        domain=[("is_delivery", "=", True)],
    )
    delivery_ids = fields.One2many(
        "resource.activity.delivery",
        "activity_id",
        string="Delivery",
        ondelete="set null",
    )
    delivery_place = fields.Char(string="Delivery place")
    delivery_time = fields.Datetime(string="Delivery time")
    pickup_place = fields.Char(string="Pick up place")
    pickup_time = fields.Datetime(string="Pick up time")

    @api.model
    def create(self, vals):
        if "need_delivery" in vals and vals.get("need_delivery"):
            vals["delivery_ids"] = [
                (0, False, {"delivery_type": "delivery"}),
                (0, False, {"delivery_type": "pickup"}),
            ]
        return super(ResourceActivity, self).create(vals)

    @api.multi
    def write(self, vals):
        for activity in self:
            # reset delivery ids
            if "need_delivery" in vals and not vals.get("need_delivery"):
                vals["delivery_ids"] = [(5,)]
            else:
                vals["delivery_ids"] = [
                    (5, False, False),
                    (0, False, {"delivery_type": "delivery"}),
                    (0, False, {"delivery_type": "pickup"}),
                ]

            if activity.sale_orders:
                if "need_delivery" in vals and not vals.get("need_delivery"):
                    vals["delivery_place"] = ""
                    vals["delivery_time"] = False
                    vals["pickup_place"] = ""
                    vals["pickup_time"] = False
                    vals["delivery_product_id"] = False

                watches = (
                    "need_delivery",
                    "delivery_product_id",
                )
                if any(map(lambda var: var in vals, watches)):
                    vals["need_push"] = True

        return super(ResourceActivity, self).write(vals)

    @api.onchange(
        "date_start",
        "need_delivery",
        "delivery_time",
        "set_allocation_span",
    )
    def _onchange_allocation_start(self):
        """
        Sets allocation start to the soonest date between
        date_start and delivery_time.
        resource_allocation_start can however still be
        manually set by user if set_allocation_span is true.
        """
        if not self.date_start:
            return

        if self.need_delivery:
            if self.set_allocation_span:
                start = Datetime.from_string(self.date_start) - timedelta(
                    minutes=90
                )
            else:
                # get utc, set it to local time midnight
                #  send it back as utc because we send fields
                #  directly to the frontend
                start = (
                    self.delivery_time
                    if self.delivery_time
                    else self.date_start
                )
                start = self._trunc_day(start)
            self.resource_allocation_start = Datetime.to_string(start)
        else:
            self.resource_allocation_start = self.date_start

        @api.one
        @api.constrains(
            "need_delivery",
            "delivery_time",
            "pickup_time",
        )
        def _check_booked_resources_blocks_delivery_fields(self):
            if self.booked_resources:
                raise ValidationError(
                    _(
                        "You cannot modify activity delivery information "
                        "when a resource is already booked. You must either "
                        "delete this activity and create a new one or "
                        "release all booked resources for this activity. "
                    )
                )

    def _prepare_lines(self):
        prepared_lines = super(ResourceActivity, self)._prepare_lines()
        if self.need_delivery:
            registrations = self.registrations.filtered(
                lambda r: r.state != "cancelled" and r.quantity_needed > 0
            )
            for registration in registrations:
                if self.partner_id:
                    partner = self.partner_id.id
                else:
                    partner = registration.attendee_id.id

                prepared_lines.append(
                    OrderLine(
                        partner,
                        self.delivery_product_id,
                        registration.quantity_needed,
                        "delivery",
                        registration,
                    )
                )
        return prepared_lines

    def _create_order_line(self, order, line_type, product, qty):
        order_line = super(ResourceActivity, self)._create_order_line(
            order, line_type, product, qty
        )
        if line_type == "delivery":
            order_line.resource_delivery = True

    # fixme never used ??
    # def update_delivery_line(self, activity, sale_order_id, nb_delivery):
    #     delivery_line = sale_order_id.order_line.filtered(
    #         lambda record: record.resource_delivery
    #     )
    #     line_vals = {"resource_delivery": True}
    #
    #     self.update_order_line(
    #         sale_order_id,
    #         activity.need_delivery,
    #         line_vals,
    #         delivery_line,
    #         nb_delivery,
    #         activity.delivery_product_id,
    #     )
