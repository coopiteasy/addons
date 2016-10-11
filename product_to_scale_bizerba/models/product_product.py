# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp.osv import fields
from openerp.osv.orm import Model


class product_product(Model):
    _inherit = 'product.product'
    _order = 'scale_sequence, default_code, name_template'

    _SCALE_UOM_TYPE_WEIGHTABLE = 'P'
    _SCALE_UOM_TYPE_FIXED = 'F'

    # Compute Section
    def _compute_scale_uom_type(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context):
            if product.uom_id.category_id.scale_weight:
                res[product.id] = self._SCALE_UOM_TYPE_WEIGHTABLE
            else:
                res[product.id] = self._SCALE_UOM_TYPE_FIXED
        return res

    # Column Section
    _columns = {
        'scale_group_id': fields.many2one(
            'product.scale.group', string='Scale Group'),
        'scale_sequence': fields.integer(
            string='Scale Sequence'),
        'scale_uom_type': fields.function(
            _compute_scale_uom_type, type='char', help="Technical field used"
            " to indicate that the product has a fixed weight (F)"
            " or not (P).\nThis field is computed based on the UoM of the"
            " product", string='Scale UoM Type'),
        'scale_tare_weight': fields.float(
            string='Scale Tare Weight', help="Set here Constant tare weight"
            " for the given product. This tare will be substracted when"
            " the product is weighted. Usefull only for weightable product.\n"
            "The tare is defined with kg uom."),
    }

    # Custom Section
    def _send_to_scale_bizerba(self, cr, uid, action, product, context=None):
        log_obj = self.pool['product.scale.log']
        log_obj.create(cr, uid, {
            'log_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scale_system_id': product.scale_group_id.scale_system_id.id,
            'product_id': product.id,
            'action': action,
            }, context=context)

    def _check_vals_scale_bizerba(self, cr, uid, vals, product, context=None):
        system = product.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        vals_fields = vals.keys()
        return set(system_fields).intersection(vals_fields)

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        if vals.get('scale_group_id', False):
            send_to_scale = True
        res = super(product_product, self).create(
            cr, uid, vals, context=context)
        product = self.browse(cr, uid, res, context=context)
        self._send_to_scale_bizerba(
            cr, uid, 'create', product, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        defered = {}
        for product in self.browse(cr, uid, ids, context=context):
            ignore = not product.scale_group_id\
                and not 'scale_group_id' in vals.keys()
            
            if not ignore:
                if not product.scale_group_id:
                    # (the product is new on this group)
                    defered[product.id] = 'create'
                else:
                    if vals.get('scale_group_id', False) and (
                            vals.get('scale_group_id', False)
                                != product.scale_group_id):
                            # (the product has moved from a group to another)
                            # Remove from obsolete group
                            self._send_to_scale_bizerba(
                                cr, uid, 'unlink', product, context=context)
                            # Create in the new group
                            defered[product.id] = 'create'
                    elif self._check_vals_scale_bizerba(
                            cr, uid, vals, product, context=context):
                        # Data related to the scale 
                        defered[product.id] = 'write'

        res = super(product_product, self).write(
            cr, uid, ids, vals, context=context)

        for product_id, action in defered.iteritems():
            product = self.browse(cr, uid, product_id, context=context)
            self._send_to_scale_bizerba(
                cr, uid, action, product, context=context)

        return res

    def unlink(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            if product.scale_group_id:
                self._send_to_scale_bizerba(
                    cr, uid, 'unlink', product, context=context)
        return super(product_product, self).unlink(
            cr, uid, ids, context=context)
