# -*- coding: utf-8 -*-
# © 2017 Houssine BAKKALI, Coop IT Easy
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp

class product_product(models.Model):
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
            self._send_to_scale_bizerba('create', product)
        return True

    @api.multi
    def send_scale_write(self):
        for product in self:
            self._send_to_scale_bizerba('write', product)
        return True

    @api.multi
    def send_scale_unlink(self):
        for product in self:
            self._send_to_scale_bizerba('unlink', product)
        return True

    # Custom Section
    def _send_to_scale_bizerba(self, action, product):
        log_obj = self.env['product.scale.log']
        log_obj.create({
            'log_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scale_system_id': product.scale_group_id.scale_system_id.id,
            'product_id': product.id,
            'action': action,
            })

    def _check_vals_scale_bizerba(self, vals, product):
        system = product.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        vals_fields = vals.keys()
        return set(system_fields).intersection(vals_fields)

    # Overload Section
    @api.model
    def create(self, vals):
        send_to_scale = vals.get('scale_group_id', False)
        res = super(product_product, self).create(
            cr, uid, vals, context=context)
        if send_to_scale:
            product = self.browse(res)
            self._send_to_scale_bizerba('create', product)
        return res
    
    @api.multi
    def write(self):
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
                        self._send_to_scale_bizerba('unlink', product)
                        # Create in the new group
                        defered[product.id] = 'create'
                    elif self._check_vals_scale_bizerba(vals, product):
                        # Data related to the scale
                        defered[product.id] = 'write'

        res = super(product_product, self).write(vals)

        for product_id, action in defered.iteritems():
            product = self.browse(product_id)
            self._send_to_scale_bizerba(action, product)

        return res
    
    @api.multi
    def unlink(self):
        for product in self:
            if product.scale_group_id:
                self._send_to_scale_bizerba(
                    cr, uid, 'unlink', product, context=context)
        return super(product_product, self).unlink()