# -*- coding: utf-8 -*-

from openerp import api, fields, models


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
            partner_orders.sorted()
            if len(partner_orders) > 0:
                partner.last_order = partner_orders[0].date_order
