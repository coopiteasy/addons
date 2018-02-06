# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

from openerp.exceptions import UserError


class SubscriptionRequest(models.Model):
    _inherit = "product.subscription.request"
    
    
    def get_available_carriers(self, partner_id):
        carriers = self.env['delivery.carrier'].search([('shipping_enabled','=',True)])
        available_carriers = []
        for carrier in carriers:
            if carrier.verify_carrier(partner_id):
                available_carriers.append(carrier)
        
        return available_carriers
    
    carrier_id = fields.Many2one("delivery.carrier", domain=[('shipping_enabled','=',True)], string="Delivery Method")

   
    @api.onchange('carrier_id')
    def onchange_carrier(self):
        if self.carrier_id:
            if not self.carrier_id.verify_carrier(self.subscriber):
                raise UserError(_('This carrier is not available for this subscriber. Please select another one'))
            else:
                available_carriers = self.get_available_carriers(self.subscriber)
                if available_carriers:
                    self.carrier_id = available_carriers[0]
    
    def create_invoice(self, partner, vals={}):
        if self.carrier_id:
            vals['carrier_id']= self.carrier_id.id 
        else:
            available_carriers = self.get_available_carriers(self.subscriber)
            if available_carriers:
                self.carrier_id = available_carriers[0]
                vals['carrier_id']= self.carrier_id.id
        vals['address_shipping_id'] = self.subscriber.id
        invoice = super(SubscriptionRequest, self).create_invoice(partner, vals)
        invoice.delivery_set(self.subscription_template.product_qty)
        
        return invoice