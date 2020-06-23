import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = "pos.session"

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
            taxes = line.tax_ids.filtered(
                lambda t: t.company_id.id == company_id
            )
            if fiscal_position:
                taxes = fiscal_position.map_tax(
                    taxes, line.product_id, partner
                )
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = taxes.compute_all(
                price,
                currency,
                line.qty,
                product=line.product_id,
                partner=partner or False,
            )["taxes"]
            for tax in taxes:
                if group_taxes.get(tax.get("id")):
                    group_taxes[tax.get("id")] += tax.get("amount", 0.0)
                else:
                    group_taxes[tax.get("id")] = tax.get("amount", 0.0)
        amount_tax = 0.0
        for value in group_taxes.values():
            amount_tax += currency.round(value)

        taxes_diff = abs(order.amount_tax != amount_tax)
        if taxes_diff != 0:
            logging.info(
                (
                    "Taxes calculated in POS client and in backend "
                    "don't match. There is a difference of %.2f on the "
                    "pos order %s."
                )
                % (taxes_diff, order.name)
            )
            order.amount_tax = amount_tax
            order.amount_total = amount_tax + amount_untaxed

    @api.multi
    def fix_pos_orders_taxes(self):
        for session in self:
            if session.state == "closing_control":
                rounding_method = (
                    session.config_id.company_id.tax_calculation_rounding_method
                )
                orders = session.order_ids.filtered(
                    lambda order: order.state == "paid"
                )

                for order in orders:
                    if rounding_method == "round_globally":
                        self._amount_order_tax(order)
        return True
