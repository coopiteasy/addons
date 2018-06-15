# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

from openerp.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    firstname = fields.Char('First Name')
    lastname = fields.Char('Last Name')
    subscriber = fields.Boolean(string="Subscriber")
    old_subscriber = fields.Boolean(string="Old subscriber")
    subscriptions = fields.One2many('product.subscription.object','subscriber', string="Subscription")
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    subscription = fields.Boolean(string="Subscription")
    product_qty = fields.Integer(string="Product quantity")
    
class SubscriptionTemplate(models.Model):
    _name = "product.subscription.template"
    
    name = fields.Char(string="Subscription name", copy=False, required=True)
    description = fields.Char(string="Description")
    product_qty = fields.Integer(string="Subscription quantity", required=True, help="This is the quantity of product that will be allocated by this subscription")
    price = fields.Float(related='product.lst_price', string="Subscription price", readonly=True)
    publish = fields.Boolean(string="Publish on website")
    product = fields.Many2one('product.template', string='Product', 
                              domain=[('subscription','=',True)],required=True)
    analytic_distribution = fields.Many2one('account.analytic.distribution', string="Analytic distribution")
    journal = fields.Many2one('account.journal',string='Journal',required=True,domain=[('type','=','sale')])

class SubscriptionRequest(models.Model):
    _name = "product.subscription.request"
    
    _order = "subscription_date desc, id desc"
    
    name = fields.Char(string="Name", copy=False)
    gift  = fields.Boolean(string="Gift?")
    sponsor = fields.Many2one('res.partner', string="Sponsor")
    subscriber = fields.Many2one('res.partner', string="Subscriber", required=True)
    subscription_date = fields.Date(string='Subscription request date', default=fields.Date.today())
    payment_date = fields.Date(string="Payment date", readonly=True)
    invoice = fields.Many2one('account.invoice', string="Invoice", readonly=True, copy=False)
    state = fields.Selection([('draft','Draft'),
                              ('sent','Sent'),
                              ('paid','Paid'),
                              ('cancel','Cancelled')], string="State", default="draft")
    subscription = fields.Many2one('product.subscription.object', string="Subscription", readonly=True, copy=False)
    subscription_template = fields.Many2one('product.subscription.template',string="Subscription template",required=True)

    def _get_account(self, partner, product):
        account = product.property_account_income_id or product.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') % \
                            (product.name, product.id, product.categ_id.name))

        fpos = partner.property_account_position_id
        if fpos:
            account = fpos.map_account(account)
        return account

    def _prepare_invoice_line(self, product, partner, qty):
        self.ensure_one()
        res = {}
        
        account = self._get_account(partner, product)

        res = {
            'name': product.name,
            'account_id': account.id,
            'price_unit': product.lst_price,
            'quantity': qty,
            'uom_id': product.uom_id.id,
            'product_id': product.id or False,
            'invoice_line_tax_ids': [(6, 0, product.taxes_id.ids)]
        }
        return res
    
    def send_invoice(self, invoice):
        invoice_email_template = self.env.ref('account.email_template_edi_invoice', False)
        
        # we send the email with invoice in attachment 
        invoice_email_template.send_mail(invoice.id)
        invoice.sent = True
        
    def create_invoice(self, partner, vals={}):
        # creating invoice and invoice lines
        vals.update({'partner_id':partner.id, 
                'subscription':True,
                'journal_id':self.subscription_template.journal.id,
                'type': 'out_invoice'})
        
        invoice = self.env['account.invoice'].create(vals)
        
        vals = self._prepare_invoice_line(self.subscription_template.product, partner, 1)
        vals['invoice_id'] = invoice.id
        
        if self.subscription_template.analytic_distribution:
            vals['analytic_distribution_id'] = self.subscription_template.analytic_distribution.id
        
        line = self.env['account.invoice.line'].create(vals)
        
        return invoice
    
    @api.model
    def create(self,vals):
        prod_sub_req_seq = self.env.ref('product_subscription.sequence_product_subscription_request', False)
        
        prod_sub_num = prod_sub_req_seq.next_by_id()
        vals['name'] = prod_sub_num
        
        return super(SubscriptionRequest,self).create(vals)
    
    @api.one
    def validate_request(self):
        partner = self.subscriber
        # if it's a gift then the sponsor is set on the invoice
        if self.gift:
            partner = self.sponsor
        
        invoice = self.create_invoice(partner,{})
        invoice.compute_taxes()
        
        invoice.signal_workflow('invoice_open')
        
        self.send_invoice(invoice)
        
        self.write({'state':'sent','invoice':invoice.id})

    @api.one
    def cancel_request(self):
        self.state = 'cancel'
        
    @api.one
    def action_draft(self):
        self.state = 'draft'
    
    @api.model
    def _validate_pending_request(self):
        pending_request_list = self.search([('state','=','draft')])
        
        for pending_request in pending_request_list:
            try:
                pending_request.validate_request()
            except UserError:
                continue


class SubscriptionObject(models.Model):
    _name = "product.subscription.object"
    
    @api.model
    def _compute_subscriber(self):
        sub_to_renew = self.search([('counter','=',1),('state','!=','renew')])
        sub_to_renew.write({'state':'renew'})
        sub_to_terminate = self.search([('counter','=',0),('state','!=','terminated')])
        sub_to_terminate.write({'state':'terminated'})
        
        subscribers = self.search([('state','=','terminated')]).mapped('subscriber')
        to_deactivate = subscribers.filtered('subscriber')
        if len(to_deactivate) > 0:
            to_deactivate.write({'subscriber':False, 'old_subscriber':True})
        
    name = fields.Char(string="Name", copy=False, required=True)
    subscriber = fields.Many2one('res.partner', string="Subscriber", required=True)
    counter = fields.Float(string="Counter")
    subscribed_on = fields.Date(string="First subscription date")
    state = fields.Selection([('draft','Draft'),
                              ('waiting','Waiting'),
                              ('ongoing','Ongoing'),
                              ('renew','Need to Renew'),
                              ('terminated','Terminated')],string="State", default="draft")
    subscription_requests = fields.One2many('product.subscription.request','subscription', string="Subscription request")