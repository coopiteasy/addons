# -*- coding: utf-8 -*-
from openerp import api, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _amount_order_tax(self, order):
        currency = order.pricelist_id.currency_id
        fiscal_position = order.fiscal_position_id
        company_id = order.company_id.id
        partner = order.partner_id
        group_taxes = {}
        amount_untaxed = 0
        for line in order.lines:
            amount_untaxed += line.price_subtotal
            taxes = line.tax_ids.filtered(lambda t: t.company_id.id == company_id)
            if fiscal_position:
                taxes = fiscal_position.map_tax(taxes,
                                                line.product_id, partner)
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = taxes.compute_all(price, currency, line.qty,
                                      product=line.product_id,
                                      partner=partner or False)['taxes']
            for tax in taxes:
                if group_taxes.get(tax.get('id')):
                    group_taxes[tax.get('id')] += tax.get('amount', 0.0)
                else:
                    group_taxes[tax.get('id')] = tax.get('amount', 0.0)
        amount_tax = 0.0
        for value in group_taxes.values():
            amount_tax += currency.round(value)

        return amount_tax

    @api.depends('statement_ids',
                 'lines.price_subtotal_incl',
                 'lines.discount')
    def _compute_amount_all(self):
        for order in self:
            company = order.session_id.config_id.company_id
            rounding_method = company.tax_calculation_rounding_method

            order.amount_paid = order.amount_return = order.amount_tax = 0.0
            currency = order.pricelist_id.currency_id
            order.amount_paid = sum(payment.amount for payment in order.statement_ids)
            order.amount_return = sum(payment.amount < 0 and payment.amount or 0 for payment in order.statement_ids)

            if rounding_method == 'round_globally':
                order.amount_tax = self._amount_order_tax(order)
            else:
                order.amount_tax = currency.round(sum(self._amount_line_tax(line, order.fiscal_position_id) for line in order.lines))

            amount_untaxed = currency.round(sum(line.price_subtotal for line in order.lines))
            order.amount_total = order.amount_tax + amount_untaxed