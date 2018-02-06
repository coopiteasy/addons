# -*- coding: utf-8 -*-

import logging
from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    
    def _get_shipping_country(self,countries):
        country_ids = set()
        #values['shipping_countries'] = values['countries']

        delivery_carriers = self.search([('shipping_enabled', '=', True)])
        for carrier in delivery_carriers:
            if not carrier.country_ids:
                return False
            # Authorized shipping countries
            country_ids = country_ids|set(carrier.country_ids.ids)

        shipping_countries = countries.filtered(lambda r: r.id in list(country_ids))
        return shipping_countries
    
    @api.multi
    def get_price_available_invoice(self, invoice):
        self.ensure_one()
        total = weight = volume = quantity = 0
        total_delivery = 0.0
        ProductUom = self.env['product.uom']
        for line in invoice.invoice_line_ids:
            if line.is_delivery:
                total_delivery += line.price_subtotal
            if not line.product_id or line.is_delivery:
                continue
            qty = ProductUom._compute_qty(line.uom_id.id, line.quantity, line.product_id.uom_id.id)
            weight += (line.product_id.weight or 0.0) * qty
            volume += (line.product_id.volume or 0.0) * qty
            quantity += qty
        total = (invoice.amount_total or 0.0) - total_delivery

        total = invoice.currency_id.with_context(date=invoice.date_invoice).compute(total, invoice.company_id.currency_id)

        return self.get_price_from_picking(total, weight, volume, quantity)