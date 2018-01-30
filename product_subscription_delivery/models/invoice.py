# -*- coding: utf-8 -*-
from datetime import datetime
from openerp import models, fields, api, _

from openerp.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    carrier_id = fields.Many2one('delivery.carrier', string="Delivery Method")
    
    @api.multi
    def _delivery_unset(self):
        self.env['account.invoice.line'].search([('invoice_id', 'in', self.ids), ('is_delivery', '=', True)]).unlink()

    @api.multi
    def delivery_set(self, quantity=1):

        # Remove delivery lines from the invoice
        self._delivery_unset()

        for invoice in self:
            carrier = invoice.carrier_id
            if carrier:
                if invoice.state not in ('draft', 'sent'):
                    raise UserError(_('The invoice state have to be draft to add delivery lines.'))

                # The delivery type is based on fixed price
                carrier = invoice.carrier_id.verify_carrier(invoice.partner_id)
                if not carrier:
                    raise UserError(_('No carrier matching.'))
                price_unit = carrier.get_price_available_invoice(invoice)
                if invoice.company_id.currency_id.id != invoice.currency_id.id:
                    price_unit = invoice.company_id.currency_id.with_context(date=invoice.date_invoice).compute(price_unit, invoice.currency_id)

                invoice._create_delivery_line(carrier, price_unit, quantity)

            else:
                raise UserError(_('No carrier set for this invoice.'))

        return True

    def _create_delivery_line(self, carrier, price_unit, quantity):
        invoice_line_obj = self.env['account.invoice.line']

        # Apply fiscal position
        taxes = carrier.product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(taxes).ids
        
        account = self.env['product.subscription.request']._get_account(self.partner_id, carrier.product_id)
        
        # Create the sale order line
        values = {
            'invoice_id': self.id,
            'name': carrier.name,
            'quantity': quantity,
            'uom_id': carrier.product_id.uom_id.id,
            'account_id': account.id,
            'product_id': carrier.product_id.id,
            'price_unit': price_unit,
            'invoice_line_tax_ids': [(6, 0, taxes_ids)],
            'is_delivery': True,
        }
        if self.invoice_line_ids:
            values['sequence'] = self.invoice_line_ids[-1].sequence + 1
        return invoice_line_obj.sudo().create(values)

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    
    is_delivery = fields.Boolean(string="Is a Delivery", default=False)