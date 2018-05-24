# -*- coding: utf-8 -*-

from openerp import api, fields, models
import datetime as dt

class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_order = fields.Date(
        string="Last Order",
        compute="compute_last_order_date",
        store=True
    )

    last_contact_date = fields.Date(
        string="Last Contact Date"
    )

    last_contact_comment = fields.Char(
        string="Last Contact Comment"
    )

    sale_frequency = fields.Char(
        string="Sale Order Frequency",
        compute="compute_last_order_date",
        store=True,
        help="Compute the average time between two orders over the last 12 "
             "months."
    )

    @api.multi
    @api.depends('sale_order_ids')
    def compute_last_order_date(self):
        for partner in self:
            partner_orders = (
                partner
                .sale_order_ids
                .filtered(lambda r: r.state not in ['cancel', 'exception']))
            childs_orders = (
                partner
                .mapped('child_ids.sale_order_ids')
                .filtered(lambda r: r.state not in ['cancel', 'exception']))
            partner_orders = partner_orders + childs_orders
            partner_orders = partner_orders.sorted()

            # last orders
            if len(partner_orders) > 0:
                partner.last_order = partner_orders[0].date_order
            else:
                partner.last_order = None

            # sale frequency
            last_year = dt.datetime.today() - dt.timedelta(days=365)
            order_dates = partner_orders.mapped('date_order')
            order_dates = map(fields.Datetime.from_string, order_dates)
            order_dates = filter(lambda d: d > last_year, order_dates)
            order_dates = list(sorted(order_dates))

            if len(order_dates) >= 2:
                order_date_deltas = [d2 - d1 for d1, d2 in zip(order_dates[:-1], order_dates[1:])]
                delta_sum = sum(order_date_deltas, dt.timedelta(0))
                average_delta = delta_sum / len(order_date_deltas)

                partner.sale_frequency = "%s days" % average_delta.days

            else:
                partner.sale_frequency = None
