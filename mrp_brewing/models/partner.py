# -*- coding: utf-8 -*-

from openerp import api, fields, models
import datetime as dt

_parse_date = fields.Datetime.from_string


def _last_year():
    return dt.datetime.today() - dt.timedelta(days=365)


def filter_last_year_orders(partner_orders):
    last_year_orders = partner_orders.filtered(
        lambda po: _parse_date(po.date_order) > _last_year()
    )
    return last_year_orders


def compute_last_order(partner_orders):
    partner_orders = partner_orders.sorted()
    if len(partner_orders) > 0:
        return partner_orders[0].date_order
    else:
        return None


def compute_sale_frequency(partner_orders):
    partner_orders = filter_last_year_orders(partner_orders)
    order_dates = partner_orders.mapped('date_order')
    order_dates = map(_parse_date, order_dates)
    order_dates = list(sorted(order_dates))

    if len(order_dates) >= 2:
        order_date_deltas = [
            d2 - d1 for d1, d2 in zip(order_dates[:-1], order_dates[1:])
        ]
        delta_sum = sum(order_date_deltas, dt.timedelta(0))
        average_delta = delta_sum / len(order_date_deltas)

        return "%s days" % average_delta.days

    else:
        return None


def compute_crate_per_order(partner_orders):
    partner_orders = filter_last_year_orders(partner_orders)
    crate_lines = (
        partner_orders
        .mapped('order_line')
        .filtered(lambda ol: ol.product_id.is_crate))

    if crate_lines:
        nb_crates = sum(crate_lines.mapped('qty_invoiced'))
        return nb_crates / len(partner_orders)
    else:
        return None


def compute_crate_per_month(partner_orders):
    last_year_orders = filter_last_year_orders(partner_orders)

    crate_lines = (
        last_year_orders
        .mapped('order_line')
        .filtered(lambda ol: ol.product_id.is_crate))

    if crate_lines:
        nb_crates = sum(crate_lines.mapped('qty_invoiced'))

        order_dates = map(_parse_date, partner_orders.mapped('date_order'))
        first_order_date = sorted(order_dates, reverse=True).pop()

        # average on the last 12 months if customer has ordered before the last
        # 12 month. Compute average since the first order otherwise.
        if first_order_date < _last_year():
            nb_months = 12
        else:
            nb_months = ((dt.datetime.today() - first_order_date).days / 31) + 1

        return nb_crates / nb_months
    else:
        return None


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_order = fields.Date(
        string="Last Order",
        compute="_compute_sales_statistics",
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
        compute="_compute_sales_statistics",
        store=True,
        help="Average time between two orders over the last 12 months."
    )
    
    crate_per_order = fields.Float(
        string="Crates Bought per Sale Order",
        compute="_compute_sales_statistics",
        store=True,
        help="Average number of crates bought per order over the last 12 months."
    )

    crate_per_month = fields.Float(
        string="Crates Bought per Month",
        compute="_compute_sales_statistics",
        store=True,
        help="Average number of crates bought per month over the last 12 months."
    )

    @api.multi
    @api.depends('sale_order_ids')
    def _compute_sales_statistics(self):
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

            partner.last_order = compute_last_order(partner_orders)
            partner.sale_frequency = compute_sale_frequency(partner_orders)
            partner.crate_per_order = compute_crate_per_order(partner_orders)
            partner.crate_per_month = compute_crate_per_month(partner_orders)
