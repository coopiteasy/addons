# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class product_scale_log(Model):
    _name = 'product.scale.log'
    _inherit = 'ir.needaction_mixin'

    _EXTERNAL_SIZE_ID_LEFT = 6

    _EXTERNAL_SIZE_ID_RIGHT = 6

    _DELIMITER = '#'

    _ACTION_SELECTION = [
        ('create', 'Creation'),
        ('write', 'Update'),
        ('unlink', 'Deletion'),
    ]

    # Compute Section
    def _compute_action_code(
            self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context=context):
            if log.action in ['create', 'write']:
                res[log.id] = 'C'
            elif log.action in ['unlink']:
                res[log.id] = 'S'
        return res

    def _compute_product_text(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context):
            if not log.product_id:
                res[log.id] = False
                continue
            group = log.product_id.scale_group_id
            current_line = log.action_code + self._DELIMITER

            # Set custom fields
            for product_line in group.scale_system_id.product_line_ids:
                print ">>>>>>>>>>>>>>>>>>>>"
                print product_line.type
                print product_line.code
                print product_line.name
                if product_line.type == 'constant':
                    current_line += product_line.constant_value
                elif product_line.type == 'id':
                    current_line += str(log.product_id.id)
                else:
                    value = getattr(log.product_id, product_line.field_id.name)
                    if product_line.type == 'numeric':
                        current_line += str(value)
                        # TODO manage round and coefficient
                    if product_line.type == 'char':
                        current_line += str(value)
                        # TODO manage split method
                    if product_line.type == 'one2many':
                        pass
                        # TODO
                current_line += product_line.delimiter
            res[log.id] = current_line
        return res


    def _compute_external_text(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context):
            if not log.product_line_id:
                res[log.id] = False
                continue
                # TODO, manage external_text on product
            current_line = log.action_code + self._DELIMITER
            

    # Column Section
    _columns = {
        'log_date': fields.datetime('Log Date', required=True),
        'scale_system_id': fields.many2one(
            'product.scale.system', string='Scale System', required=True),
        'product_id': fields.many2one(
            'product.product', string='Product'),
        'product_text': fields.function(
            _compute_product_text, type='text', string='Product Text',
            store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'product_id'], 10)}),
        'scale_product_line_id': fields.many2one(
            'product.scale.system.product.line', string='Scale product Line'),
        'external_text': fields.function(
            _compute_external_text, type='text',
            string='External Text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'scale_product_line_id',
                        'product_id'], 10)}),
        'action': fields.selection(
            _ACTION_SELECTION, string='Action', required=True),
        'action_code': fields.function(
            _compute_action_code, string='Action Code'),
        'sent': fields.boolean(string='Is Sent'),
    }

    # View Section
    def _needaction_count(self, cr, uid, domain=None, context=None):
        return len(
            self.search(cr, uid, [('sent', '=', False)], context=context))

    # Custom Section
    def send_log(self, cr, uid, context=None):
        log_ids = self.search(
            cr, uid, [('sent', '=', False)], order='log_date', context=context)
        for log in self.browse(cr, uid, log_ids, context=context):
            print "TODO : Send %s"
            # TODO
            # Send data to the correct FTP, based on scale_system_id
            self.write(cr, uid, [log.id], {'sent': True}, context=context)
