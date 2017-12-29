# -*- coding: utf-8 -*-
from datetime import datetime
from openerp import models, fields, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    subscription = fields.Boolean(string="Subscription")
    product_subscription_request = fields.One2many('product.subscription.request','invoice', string="Product subscription")
    
    def process_subscription(self,effective_date):
        # set the subscription request to paid
        req_vals = {'state':'paid',
                'payment_date':effective_date}
        
        sub_req = self.product_subscription_request
        sub_template = sub_req.subscription_template
        # check if there is already an ongoing or an old subscription 
        # tied to the subscriber
        subscriber = self.product_subscription_request.subscriber
        # allocate the product quantity to the subscriber
        if len(subscriber.subscriptions) > 0:
            # there is an existing subscription
            subscription = subscriber.subscritions[0]
            sub_vals = {'state':'ongoing',
                        'counter':subscription.counter + sub_template.product_qty}
            subscription.write(sub_vals)
            req_vals['subscription'] = subscription.id
        else:
            # no subscription found for this subscriber. We need to create one
            prod_sub_seq = self.env.ref('product_subscription.sequence_product_subscription', False)
        
            prod_sub_num = prod_sub_seq.next_by_id()
            sub_vals = {'name':prod_sub_num,
                     'subscriber':subscriber.id,
                     'subscribed_on':effective_date,
                     'counter':sub_template.product_qty,
                     'state':'ongoing'}
            subscription = self.env['product.subscription.object'].create(sub_vals)
            req_vals['subscription'] = subscription.id
            subscriber.write({'subscriber':True})
        sub_req.write(req_vals)
        return True
    
    @api.multi                
    def confirm_paid(self):
        for invoice in self:
            super(AccountInvoice, invoice).confirm_paid()
            if invoice.subscription and invoice.type == 'out_invoice':
                effective_date = datetime.now().strftime("%d/%m/%Y")
                #take the effective date from the payment. by default the confirmation date is the payment date
                if invoice.payment_move_line_ids :
                    move_line = invoice.payment_move_line_ids[0]
                    effective_date = move_line.date
                
                invoice.process_subscription(effective_date)        
        return True