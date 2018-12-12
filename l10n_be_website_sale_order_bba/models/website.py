# © 2018 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools

from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def _prepare_sale_order_values(self, partner, pricelist):
        values = super(Website, self)._prepare_sale_order_values(partner,
                                                                 pricelist)
        reference_type = partner.out_inv_comm_type
        values['reference_type'] = reference_type
        values['reference'] = self.env['account.invoice'].generate_bbacomm(
                    'out_invoice',
                    reference_type,
                    self.partner_id.id, '')['value']['reference']
        return values
