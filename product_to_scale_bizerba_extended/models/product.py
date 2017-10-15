# -*- coding: utf-8 -*-
# © 2017 Houssine BAKKALI, Coop IT Easy
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    scale_group_id = fields.Many2one(related="product_variant_ids.scale_group_id", string='Scale Group', store=True)
    scale_sequence = fields.Integer(related="product_variant_ids.scale_sequence",string='Scale Sequence', store=True)
    scale_tare_weight = fields.Float(related="product_variant_ids.scale_tare_weight",string='Scale Tare Weight', store=True,
        help="Set here Constant tare weight"
        " for the given product. This tare will be substracted when"
        " the product is weighted. Usefull only for weightable product.\n"
        "The tare is defined with kg uom.")

    # View Section
    @api.multi
    def send_scale_create(self):
        for product in self:
            product._send_to_scale_bizerba('create',True)
        return True

    @api.multi
    def send_scale_write(self):
        for product in self:
            product._send_to_scale_bizerba('write',True)
        return True

    @api.multi
    def send_scale_unlink(self):
        for product in self:
            product._send_to_scale_bizerba('unlink')
        return True

    # Custom Section
    def _send_to_scale_bizerba(self, action, send_product_image=False):
        log_obj = self.env['product.scale.log']
        log_obj.create({
            'log_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scale_system_id': self.scale_group_id.scale_system_id.id,
            'product_id': self.id,
            'action': action,
            'send_product_image': send_product_image,
            })

    def _check_vals_scale_bizerba(self, vals):
        system = self.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        vals_fields = vals.keys()
        return set(system_fields).intersection(vals_fields)

    # Overload Section
    @api.model
    def create(self, vals):
        send_to_scale = vals.get('scale_group_id', False)
        res = super(ProductTemplate, self).create(vals)
        if send_to_scale:
            product = self.browse(res)
            self._send_to_scale_bizerba('create')
        return res
    
    @api.multi
    def write(self, vals):
        defered = {}
        for product in self:
            ignore = not product.scale_group_id\
                and 'scale_group_id' not in vals.keys()
            if not ignore:
                if not product.scale_group_id:
                    # (the product is new on this group)
                    defered[product.id] = 'create'
                else:
                    if vals.get('scale_group_id', False) and (
                            vals.get('scale_group_id', False) !=
                            product.scale_group_id):
                        # (the product has moved from a group to another)
                        # Remove from obsolete group
                        product._send_to_scale_bizerba('unlink')
                        # Create in the new group
                        defered[product.id] = 'create'
                    elif product._check_vals_scale_bizerba(vals):
                        # Data related to the scale
                        defered[product.id] = 'write'
                # ticking and unticking the "can be sold" checkbox
                # trigger the corresponding product_scale_log 
                if 'sale_ok' in vals.keys():
                    if product.sale_ok and not vals.get('sale_ok', False):
                        product._send_to_scale_bizerba('unlink')
                    elif vals.get('sale_ok', False) and vals.get('sale_ok', False):
                        defered[product.id] = 'create'

        res = super(ProductTemplate, self).write(vals)

        for product_id, action in defered.iteritems():
            product = self.browse(product_id)
            product._send_to_scale_bizerba(action, True)

        return res
    
    @api.multi
    def unlink(self):
        for product in self:
            if product.scale_group_id:
                self._send_to_scale_bizerba('unlink')
        return super(ProductTemplate, self).unlink()