# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class product_scale_log(Model):
    _name = 'product.scale.log'
    _inherit = 'ir.needaction_mixin'

    _ACTION_SELECTION = [
        ('create', 'Creation'),
        ('write', 'Update'),
        ('unlink', 'Deletion'),
    ]

    def _needaction_count(self, cr, uid, domain=None, context=None):
        return len(
            self.search(cr, uid, [('sent', '=', False)], context=context))

    # Compute Section
    def _get_product_log_line(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context):
            group = log.product_id.scale_group_id
            if log.action in ['create', 'write']:
                var_list = ['C']
            else:
                var_list = ['S']
            var_list.append(group.external_id)
            var_list.append(product.id)
            for product_line in group.scale_system_id.product_lines:
                if product_line.type == 'constant':
                    var_list.append(product_line.constant_value)
                else:
                    value = getattr(log.product_id, product_line.field_id.name)
                    if product_line.type == 'numeric':
                        var_list.append(value)
                        # TODO manage round and coefficient
                    if product_line.type == 'char':
                        var_list.append(value)
                        # TODO manage split method
                    if product_line.type == 'one2many':
                        pass
                        # TODO
            res[log.id] = '#'.join(var_list)
        return res

    # Column Section
    _columns = {
        'log_date': fields.datetime('Log Date', required=True),
        'scale_system_id': fields.many2one(
            'product.scale.system', string='Scale System', required=True),
        'product_id': fields.many2one(
            'product.product', string='Product', required=True),
        'action': fields.selection(
            _ACTION_SELECTION, string='Action', required=True),
        'product_log_line': fields.function(
            _get_product_log_line, type='text', string='Product Log Line',
            store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'product_id'], 10)}),
        'sent': fields.boolean(string='Is Sent'),
    }

    # Custom Section
    def send_log(self, cr, uid, context=None):
        log_ids = self.search(
            cr, uid, [('sent', '=', False)], order='log_date', context=context)
        for log in self.browse(cr, uid, log_ids, context=context):
            print "TODO : Send %s"
            # TODO
            # Send data to the correct FTP, based on scale_system_id
            self.write(cr, uid, [log.id], {'sent': True}, context=context)
