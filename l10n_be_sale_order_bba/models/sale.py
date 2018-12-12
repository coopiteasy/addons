# © 2018 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_cr
    def init(self):
        self.env.cr.execute("SELECT id FROM sale_order"
                            " WHERE reference_type IS NULL")
        ids = (x[0] for x in self.env.cr.fetchall())
        sale_orders = self.browse(ids)
        sale_orders.write({'reference_type': 'none'})

    @api.model
    def _get_reference_type(self):
        return [('none', _('Free Reference')),
                ('bba', _('BBA Structured Communication'))]

    reference_type = fields.Selection('_get_reference_type',
                                      string='Payment Reference',
                                      required=True,
                                      readonly=True,
                                      states={'draft': [('readonly', False)]})
    reference = fields.Char(string='Vendor Reference', copy=False,
                            help="The partner reference of this invoice.",
                            readonly=True,
                            states={'draft': [('readonly', False)]})

    @api.constrains('reference', 'reference_type')
    def _check_communication(self):
        invoice_obj = self.env['account.invoice']
        for order in self:
            if order.reference_type == 'bba' and  \
                    not invoice_obj.check_bbacomm(order.reference):
                    raise ValidationError(_('Invalid BBA Structured '
                                            'Communication !'))

    @api.onchange('partner_id', 'reference_type')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        reference = False
        reference_type = 'none'
        if self.partner_id:
            reference_type = self.partner_id.out_inv_comm_type
            if reference_type:
                reference = self.env['account.invoice'].generate_bbacomm(
                    'out_invoice',
                    reference_type,
                    self.partner_id.id, '')['value']['reference']
        self.reference_type = reference_type or 'none'
        self.reference = reference
        return result

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['reference_type'] = self.reference_type or 'none'
        invoice_vals['reference'] = self.reference

        return invoice_vals
