# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import logging
from datetime import datetime

from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model

_logger = logging.getLogger(__name__)

class product_scale_log(Model):
    _inherit = 'product.scale.log'

    _EXTERNAL_SIZE_ID_RIGHT = 4

    _DELIMITER = '#'

    _ACTION_SELECTION = [
        ('create', 'Creation'),
        ('write', 'Update'),
        ('unlink', 'Deletion'),
    ]

    _ACTION_MAPPING = {
        'create': 'C',
        'write': 'C',
        'unlink': 'S',
    }

    _ENCODING_MAPPING = {
        'iso-8859-1': '\r\n',
        'cp1252': '\n',
        'utf-8': '\n',
    }

    _EXTERNAL_TEXT_ACTION_CODE = 'C'

    _EXTERNAL_TEXT_DELIMITER = '#'

    # Private Section
    def _clean_value(self, value, product_line):
        if not value:
            return ''
        elif product_line.multiline_length:
            res = ''
            current_val = value
            while current_val:
                res += current_val[:product_line.multiline_length]
                current_val = current_val[product_line.multiline_length:]
                if current_val:
                    res += product_line.multiline_separator
        else:
            res = value
        if product_line.delimiter:
            return res.replace(product_line.delimiter, '')
        else:
            return res

    def _generate_external_text(self, value, product_line, external_id, log):
        external_text_list = [
            self._EXTERNAL_TEXT_ACTION_CODE,                    # WALO Code
            log.product_id.scale_group_id.external_identity,    # ABNR Code
            external_id,                                        # TXNR Code
            self._clean_value(value, product_line),             # TEXT Code
        ]
        return self._EXTERNAL_TEXT_DELIMITER.join(external_text_list)

    # Compute Section
    def _compute_text(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context):

            group = log.product_id.scale_group_id
            product_text =\
                self._ACTION_MAPPING[log.action] + self._DELIMITER
            external_texts = []

            # Set custom fields
            for product_line in group.scale_system_id.product_line_ids:
                if product_line.field_id:
                    value = getattr(log.product_id, product_line.field_id.name)

                if product_line.type == 'id':
                    product_text += str(log.product_id.id)

                elif product_line.type == 'numeric':
                    value = tools.float_round(
                        value * product_line.numeric_coefficient,
                        precision_rounding=product_line.numeric_round)
                    product_text += str(value).replace('.0', '')

                elif product_line.type == 'text':
                    product_text += self._clean_value(value, product_line)

                elif product_line.type == 'external_text':
                    external_id = str(log.product_id.id)\
                        + str(product_line.id).rjust(
                            self._EXTERNAL_SIZE_ID_RIGHT, '0')
                    external_texts.append(self._generate_external_text(
                        value, product_line, external_id, log))
                    product_text += external_id

                elif product_line.type == 'constant':
                    product_text += self._clean_value(
                        product_line.constant_value, product_line)

                elif product_line.type == 'external_constant':
                    # Constant Value are like product ID = 0
                    external_id = str(product_line.id)

                    external_texts.append(self._generate_external_text(
                        product_line.constant_value, product_line, external_id,
                        log))
                    product_text += external_id

                elif product_line.type == 'many2one':
                    # If the many2one is defined
                    if value and not product_line.related_field_id:
                        product_text += value.id
                    elif value and product_line.related_field_id:
                        item_value = getattr(
                            value, product_line.related_field_id.name)
                        product_text +=\
                            item_value and str(item_value) or ''

                elif product_line.type == 'many2many':
                    # Select one value, depending of x2many_range
                    if product_line.x2many_range < len(value):
                        item = value[product_line.x2many_range - 1]
                        if product_line.related_field_id:
                            item_value = getattr(
                                item, product_line.related_field_id.name)
                        else:
                            item_value = item.id
                        product_text += self._clean_value(
                            item_value, product_line)

                elif product_line.type == 'product_image':
                    product_text += str(log.product_id.id) +\
                        product_line.suffix

                if product_line.delimiter:
                    product_text += product_line.delimiter
            break_line = self._ENCODING_MAPPING[log.scale_system_id.encoding]
            res[log.id] = {
                'product_text': product_text + break_line,
                'external_text': break_line.join(external_texts) + break_line,
                'external_text_display': '\n'.join(
                    [x.replace('\n', '') for x in external_texts]),
            }
        return res

    # Column Section
    _columns = {
        'send_product_image': fields.boolean(string='Send product image'),
        'product_id': fields.many2one(
            'product.template', string='Product'),
        'product_text': fields.function(
            _compute_text, type='text', string='Product Text',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'product_id'], 10)}),
        'external_text': fields.function(
            _compute_text, type='text', string='External Text',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None: ids, [
                    'scale_system_id', 'product_id', 'product_id'], 10)}),
        'external_text_display': fields.function(
            _compute_text, type='text', string='External Text (Display)',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None: ids, [
                    'scale_system_id', 'product_id', 'product_id'], 10)}),
    }
    
    def action_send_product_image(self, cr, uid, ftp, distant_folder_path, local_folder_path, product_lst, context=None):
        if not ftp:
            return False

        att_obj = self.pool['ir.attachment']
        
        for product in product_lst:
            f_name = str(product.id) + '.jpeg'
            datas = product.image.decode('base64')
            local_path = os.path.join(local_folder_path, f_name)
            distant_path = os.path.join(distant_folder_path, f_name)
            f = open(local_path, 'wb')
            f.write(datas)
            f.close()
            # Send File by FTP
            f = open(local_path, 'rb')
            ftp.storbinary('STOR ' + distant_path, f)
            f.close()
            # Delete temporary file
            os.remove(local_path)
        return True
    
    def send_log(self, cr, uid, ids, context=None):
        config_obj = self.pool['ir.config_parameter']
        folder_path = config_obj.get_param(
            cr, uid, 'bizerba.local_folder_path', context=context)

        system_map = {}
        for log in self.browse(cr, uid, ids, context=context):
            if log.scale_system_id in system_map.keys():
                system_map[log.scale_system_id].append(log)
            else:
                system_map[log.scale_system_id] = [log]

        for scale_system, logs in system_map.iteritems():

            # Open FTP Connection
            ftp = self.ftp_connection_open(
                cr, uid, logs[0].scale_system_id, context=context)
            if not ftp:
                return False

            # Generate and Send Files
            now = datetime.now()
            product_image_lst = []
            product_text_lst = []
            external_text_lst = []

            for log in logs:
                if log.send_product_image and log.product_id.image:
                    product_image_lst.append(log.product_id)
                if log.product_text:
                    product_text_lst.append(log.product_text)
                if log.external_text:
                    external_text_lst.append(log.external_text)
            self.action_send_product_image(
                cr, uid, ftp, scale_system.product_image_relative_path,
                folder_path, product_image_lst, context=context)
            self.ftp_connection_push_text_file(
                cr, uid, ftp, scale_system.csv_relative_path,
                folder_path, scale_system.external_text_file_pattern,
                external_text_lst, scale_system.encoding, context=context)
            self.ftp_connection_push_text_file(
                cr, uid, ftp, scale_system.csv_relative_path,
                folder_path, scale_system.product_text_file_pattern,
                product_text_lst, scale_system.encoding, context=context)

            # Close FTP Connection
            self.ftp_connection_close(cr, uid, ftp, context=context)

            # Mark logs as sent
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.write(
                cr, uid, [log.id for log in logs], {
                    'sent': True,
                    'last_send_date': now,
                }, context=context)
        return True
