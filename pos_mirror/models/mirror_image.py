# -*- coding: utf-8 -*-
from openerp import api, fields, models

class MirrorImage(models.Model):
    _name = 'mirror.images'
    _order = 'sequence'

    name = fields.Char()
    image = fields.Binary()
    sequence =  fields.Integer()
    description = fields.Text()

class PosConfig(models.Model):
    _inherit = "pos.config"

    mirror_image_ids = fields.Many2many("mirror.images")

class MirrorImageOrder(models.Model):
    _name = 'mirror.image.order'

    session_id = fields.Char()
    session_name = fields.Char()
    order_id = fields.Char()
    order_line = fields.Char()
    currency = fields.Char()

    @api.model
    def create_pos_data(self, orderLine=[], order_id=None, session_id=None, currency=None, session_name=None):
        # self.sudo().search([]).unlink()
        pos = self.sudo().create({
            'order_line': orderLine,
            'order_id': order_id,
            'session_id': session_id,
            'currency': currency,
            'session_name': session_name,
        })
        return {'mirror_order': pos.id}

    @api.model
    def store_pos_data(self, orderLine=[], session_id=None):
        active_mirror_order = self.sudo().search([('session_id', '=', str(session_id))], limit=1)
        if orderLine and active_mirror_order.id:
            active_mirror_order.order_line = orderLine
        return {'mirror_order': active_mirror_order.id}

    @api.model
    def delete_pos_data(self, session_id=None):
        pos = self.sudo().search([]).unlink()
        return {'mirror_order': pos}
